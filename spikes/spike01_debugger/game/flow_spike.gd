# Prototype jetable SPIKE-01 : classe statique, sans autoload, inerte tant que
# le récepteur n'a pas envoyé « start ».
class_name FlowSpike
extends RefCounted

const CAPTURE := "flowspike"
const MAX_BUFFER := 4096
const LEASE_USEC := 2_000_000

static var _registered := false
static var _enabled := false
static var _hooked := false
static var _buffer: Array = []
static var _seq := 0
static var _dropped := 0
static var _dropped_total := 0
static var _batches := 0
static var _last_contact := 0
static var _lease_expired := 0
static var _in_event := false
static var _pending := ""
static var _reentrant_dispatches := 0


static func init() -> bool:
	if _registered:
		return true
	if not EngineDebugger.is_active():
		return false
	EngineDebugger.register_message_capture(CAPTURE, Callable(FlowSpike, &"_on_message"))
	_registered = true
	_hook()
	EngineDebugger.send_message(CAPTURE + ":ready", [Time.get_ticks_usec()])
	return true


static func is_enabled() -> bool:
	return _enabled


static func get_seq() -> int:
	return _seq


static func get_dropped_total() -> int:
	return _dropped_total


static func get_batches() -> int:
	return _batches


static func get_lease_expired() -> int:
	return _lease_expired


static func shutdown() -> void:
	_enabled = false
	_buffer.clear()
	if _registered and EngineDebugger.has_capture(CAPTURE):
		EngineDebugger.unregister_message_capture(CAPTURE)
	_registered = false


static func event(probe: StringName, value: int) -> void:
	if not _enabled:
		return
	_in_event = true
	_seq += 1
	if _buffer.size() >= MAX_BUFFER:
		_dropped += 1
		_dropped_total += 1
		_in_event = false
		return
	_buffer.append([_seq, Time.get_ticks_usec(), probe, value])
	_in_event = false


static func _on_message(message: String, data: Array) -> bool:
	_last_contact = Time.get_ticks_usec()
	if _in_event:
		_reentrant_dispatches += 1
	match message:
		"start":
			_pending = "start"
		"stop":
			_pending = "stop"
		"ping":
			EngineDebugger.send_message(CAPTURE + ":pong", [data[0], Time.get_ticks_usec()])
		_:
			return false
	return true


static func _hook() -> void:
	if _hooked:
		return
	var tree := Engine.get_main_loop() as SceneTree
	if tree == null:
		return
	tree.process_frame.connect(Callable(FlowSpike, &"_flush"))
	_hooked = true


static func _flush() -> void:
	if _pending == "start":
		_pending = ""
		_enabled = true
		EngineDebugger.send_message(CAPTURE + ":started", [_seq, Time.get_ticks_usec()])
	elif _pending == "stop":
		_pending = ""
		_send_batch()
		_enabled = false
		EngineDebugger.send_message(CAPTURE + ":stopped", [_seq, _dropped_total, Time.get_ticks_usec(), OS.get_thread_caller_id(), OS.get_main_thread_id(), _reentrant_dispatches, Engine.get_process_frames()])
		return
	if _enabled and Time.get_ticks_usec() - _last_contact > LEASE_USEC:
		_enabled = false
		_buffer.clear()
		_dropped = 0
		_lease_expired += 1
		return
	if _buffer.is_empty() and _dropped == 0:
		return
	if not EngineDebugger.is_active():
		_buffer.clear()
		return
	_send_batch()


static func _send_batch() -> void:
	if _buffer.is_empty() and _dropped == 0:
		return
	_batches += 1
	EngineDebugger.send_message(CAPTURE + ":batch", [_buffer, _dropped, Time.get_ticks_usec()])
	_buffer = []
	_dropped = 0
