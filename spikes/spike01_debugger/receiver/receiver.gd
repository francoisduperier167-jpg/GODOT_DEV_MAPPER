# Récepteur jetable SPIKE-01 : joue le rôle de l'éditeur sur le canal de débogage distant.
# Scénario : start, collecte, stop, pause, redémarrage, stop, redémarrage, coupure brutale.
extends SceneTree

const PORT := 6007
const LOG_PATH := "/tmp/spike01_receiver.log"

var server := TCPServer.new()
var peer: StreamPeerTCP = null
var inbuf := PackedByteArray()
var thread_id := 0
var t0_ms := 0
var phase := "wait_conn"
var phase_ms := 0
var lines := PackedStringArray()
var counts := {}
var batches := 0
var events_received := 0
var last_seq := 0
var seq_gaps := 0
var dropped_reported := 0
var batches_after_stopped := 0
var batch_sizes: Array[int] = []
var rtts_us: Array[int] = []
var phase_events := {}
var started_count := 0
var stopped_count := 0
var next_ping_ms := 0
var disconnect_done := false


func _initialize() -> void:
	var err := server.listen(PORT, "127.0.0.1")
	t0_ms = Time.get_ticks_msec()
	_log("écoute sur %d : %s" % [PORT, error_string(err)])


func _process(_delta: float) -> bool:
	var now := Time.get_ticks_msec()
	if now - t0_ms > 30000:
		_log("délai global dépassé")
		return _finish()
	if peer == null:
		if server.is_connection_available():
			peer = server.take_connection()
			_set_phase("wait_ready")
			_log("connexion du jeu acceptée")
		elif now - t0_ms > 20000:
			_log("aucune connexion après 20 s")
			return _finish()
		return false
	if disconnect_done:
		return _finish()
	peer.poll()
	var status := peer.get_status()
	if status != StreamPeerTCP.STATUS_CONNECTED:
		_log("connexion perdue (statut %d)" % status)
		return _finish()
	var avail := peer.get_available_bytes()
	if avail > 0:
		var res: Array = peer.get_data(avail)
		if res[0] == OK:
			inbuf.append_array(res[1])
	_parse()
	_drive(now)
	return false


func _parse() -> void:
	while inbuf.size() >= 4:
		var size := inbuf.decode_u32(0)
		if inbuf.size() < 4 + size:
			return
		var payload := inbuf.slice(4, 4 + size)
		inbuf = inbuf.slice(4 + size)
		var msg = bytes_to_var(payload)
		if typeof(msg) != TYPE_ARRAY or msg.size() < 3:
			_log("message non décodable (%d octets)" % size)
			continue
		_handle(str(msg[0]), int(msg[1]), msg[2])


func _handle(name: String, tid: int, data: Array) -> void:
	thread_id = tid
	counts[name] = int(counts.get(name, 0)) + 1
	match name:
		"flowspike:ready":
			_log("« ready » reçu (thread %d)" % tid)
			if phase == "wait_ready":
				_send("flowspike:start", [])
				_set_phase("collect1")
		"flowspike:started":
			started_count += 1
			_log("« started » reçu, seq=%d" % int(data[0]))
		"flowspike:stopped":
			stopped_count += 1
			_log("« stopped » reçu, seq=%d, pertes=%d, t_jeu=%d, thread du rappel=%d, thread principal=%d, rappels réentrants jusqu'ici=%d, frame=%d" % [int(data[0]), int(data[1]), int(data[2]), int(data[3]), int(data[4]), int(data[5]), int(data[6])])
			if phase == "stopping1":
				_set_phase("pause")
			elif phase == "stopping2":
				_set_phase("pause2")
		"flowspike:batch":
			batches += 1
			var evs: Array = data[0]
			if phase == "pause" or phase == "pause2":
				batches_after_stopped += 1
				_log("LOT APRÈS STOPPED : %d événements, seq %d à %d, envoyé à t_jeu=%d" % [evs.size(), int(evs[0][0]) if evs.size() > 0 else -1, int(evs[-1][0]) if evs.size() > 0 else -1, int(data[2])])
			batch_sizes.append(evs.size())
			dropped_reported += int(data[1])
			for e in evs:
				var s := int(e[0])
				if last_seq != 0 and s != last_seq + 1:
					seq_gaps += s - last_seq - 1
				last_seq = s
			events_received += evs.size()
			phase_events[phase] = int(phase_events.get(phase, 0)) + evs.size()
		"flowspike:pong":
			rtts_us.append(Time.get_ticks_usec() - int(data[0]))


func _drive(now: int) -> void:
	if phase.begins_with("collect") and now >= next_ping_ms:
		_send("flowspike:ping", [Time.get_ticks_usec()], false)
		next_ping_ms = now + 250
	match phase:
		"collect1":
			if now - phase_ms > 2500:
				_send("flowspike:stop", [])
				_set_phase("stopping1")
		"pause":
			if now - phase_ms > 1000:
				_send("flowspike:start", [])
				_set_phase("collect2")
		"collect2":
			if now - phase_ms > 1500:
				_send("flowspike:stop", [])
				_set_phase("stopping2")
		"pause2":
			if now - phase_ms > 500:
				_send("flowspike:start", [])
				_set_phase("collect3")
		"collect3":
			if now - phase_ms > 800:
				_log("coupure brutale de la connexion pendant la collecte")
				peer.disconnect_from_host()
				disconnect_done = true


func _send(name: String, data: Array, verbose := true) -> void:
	var payload := var_to_bytes([name, thread_id, data])
	var frame := PackedByteArray()
	frame.resize(4)
	frame.encode_u32(0, payload.size())
	frame.append_array(payload)
	var err := peer.put_data(frame)
	if verbose:
		_log("envoi « %s » : %s" % [name, error_string(err)])


func _set_phase(p: String) -> void:
	phase = p
	phase_ms = Time.get_ticks_msec()
	_log("phase → " + p)


func _finish() -> bool:
	var rt := rtts_us.duplicate()
	rt.sort()
	var bs := batch_sizes.duplicate()
	bs.sort()
	_log("--- résumé ---")
	_log("messages par nom : %s" % str(counts))
	_log("lots : %d ; événements reçus : %d ; trous de séquence : %d ; pertes annoncées : %d" % [batches, events_received, seq_gaps, dropped_reported])
	_log("lots reçus après « stopped » : %d" % batches_after_stopped)
	_log("démarrages confirmés : %d ; arrêts confirmés : %d" % [started_count, stopped_count])
	_log("événements par phase : %s" % str(phase_events))
	if bs.size() > 0:
		_log("taille des lots : min %d, médiane %d, max %d" % [bs[0], bs[int(bs.size() / 2.0)], bs[bs.size() - 1]])
	if rt.size() > 0:
		_log("aller-retour ping : %d mesures, médiane %d µs, max %d µs" % [rt.size(), rt[int(rt.size() / 2.0)], rt[rt.size() - 1]])
	var f := FileAccess.open(LOG_PATH, FileAccess.WRITE)
	if f:
		f.store_string("\n".join(lines) + "\n")
		f.close()
	return true


func _log(s: String) -> void:
	var line := "[%6d ms] %s" % [Time.get_ticks_msec() - t0_ms, s]
	lines.append(line)
	print(line)
