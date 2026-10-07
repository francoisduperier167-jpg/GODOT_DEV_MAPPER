# Scène de test : émet des événements à chaque frame et écrit son état chaque seconde.
extends Node

var rate_per_frame := 20
var run_seconds := 12.0
var lazy_init := false
var frames := 0
var start_ms := 0
const STATUS_PATH := "/tmp/spike01_game_status.txt"


func _ready() -> void:
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--rate="):
			rate_per_frame = int(a.get_slice("=", 1))
		elif a.begins_with("--seconds="):
			run_seconds = float(a.get_slice("=", 1))
		elif a == "--lazy":
			lazy_init = true
	start_ms = Time.get_ticks_msec()
	if not lazy_init:
		FlowSpike.init()


func _process(_delta: float) -> void:
	frames += 1
	if lazy_init and frames == 30:
		FlowSpike.init()
	for i in rate_per_frame:
		FlowSpike.event(&"spike.probe", i)
	var elapsed := Time.get_ticks_msec() - start_ms
	if elapsed > run_seconds * 1000.0:
		_write_status("done")
		FlowSpike.shutdown()
		get_tree().quit()
	elif frames % 60 == 0:
		_write_status("running")


func _write_status(state: String) -> void:
	var f := FileAccess.open(STATUS_PATH, FileAccess.WRITE)
	if f:
		f.store_line("%s frames=%d elapsed_ms=%d debugger_active=%s enabled=%s seq=%d dropped_total=%d batches=%d lease_expired=%d" % [
			state, frames, Time.get_ticks_msec() - start_ms, EngineDebugger.is_active(),
			FlowSpike.is_enabled(), FlowSpike.get_seq(), FlowSpike.get_dropped_total(), FlowSpike.get_batches(), FlowSpike.get_lease_expired()])
		f.close()
