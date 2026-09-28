package main

import "base:runtime"
import "core:c"
import "core:c/libc"
import "core:fmt"
import "core:os"
import "core:strconv"
import "core:strings"
import "core:sys/posix"

target_time: i64
global_message: string

ANSI_RESET      :: "\x1b[0m"
ANSI_BOLD       :: "\x1b[1m"
ANSI_BOLD_RED   :: "\x1b[1;31m"
ANSI_BOLD_GREEN :: "\x1b[1;32m"
ANSI_RED        :: "\x1b[31m"
ANSI_CYAN       :: "\x1b[36m"

current_unix_time :: proc "contextless" () -> i64 {
	return cast(i64)libc.time(nil)
}

ascii_lower_char :: proc(ch: u8) -> u8 {
	if ch >= 'A' && ch <= 'Z' {
		return ch + ('a' - 'A')
	}
	return ch
}

ascii_lower_string :: proc(value: string) -> string {
	context = runtime.default_context()
	bytes := make([]u8, len(value))
	for i := 0; i < len(value); i += 1 {
		bytes[i] = ascii_lower_char(value[i])
	}
	return string(bytes)
}

is_integer :: proc(value: string) -> (int, bool) {
	parsed, ok := strconv.parse_int(value)
	if !ok {
		return 0, false
	}
	return int(parsed), true
}

join_tokens :: proc(tokens: []string, stop: int) -> string {
	context = runtime.default_context()
	if stop <= 0 {
		return ""
	}
	return strings.join(tokens[:stop], " ")
}

parse_time :: proc(args: []string) -> (string, int, bool) {
	context = runtime.default_context()
	if len(args) == 0 {
		return "Nix.", 0, false
	}

	joined := strings.join(args, " ")
	parts := strings.fields(joined)
	if len(parts) == 0 {
		return "Nix.", 0, false
	}

	unit := ""
	number_index := -1
	value := 0

	last_value, last_ok := is_integer(parts[len(parts)-1])
	if last_ok {
		number_index = len(parts) - 1
		value = last_value
	} else if len(parts) >= 2 {
		maybe_value, maybe_ok := is_integer(parts[len(parts)-2])
		if maybe_ok {
			number_index = len(parts) - 2
			value = maybe_value
			unit = ascii_lower_string(parts[len(parts)-1])
		}
	}

	if number_index < 0 {
		return "Nix.", 0, false
	}

	message_end := number_index
	if message_end > 0 && ascii_lower_string(parts[message_end-1]) == "in" {
		message_end -= 1
	}

	message := strings.trim_space(join_tokens(parts, message_end))
	if message == "" {
		message = "Der Tee ist fertig!"
	}

	if unit == "" {
		return message, value * 60, true
	}

	switch unit {
	case "s", "sek", "sekunde", "sekunden", "sec", "second", "seconds":
		return message, value, true
	case "m", "min", "minute", "minuten", "minutes":
		return message, value * 60, true
	case "h", "std", "stunde", "stunden", "hour", "hours":
		return message, value * 3600, true
	case "t", "tag", "tage", "tagen", "d", "day", "days":
		return message, value * 86400, true
	}

	return message, value * 60, true
}

shell_escape :: proc(value: string) -> string {
	context = runtime.default_context()
	if len(value) == 0 {
		return "''"
	}

	buffer := make([dynamic]u8, 0, len(value)+16)
	append(&buffer, "'")
	for i := 0; i < len(value); i += 1 {
		if value[i] == '\'' {
			append(&buffer, "'\\''")
		} else {
			append(&buffer, value[i])
		}
	}
	append(&buffer, "'")
	return string(buffer[:])
}

applescript_escape :: proc(value: string) -> string {
	context = runtime.default_context()
	buffer := make([dynamic]u8, 0, len(value)+16)
	for i := 0; i < len(value); i += 1 {
		switch value[i] {
		case '"':
			append(&buffer, "\\\"")
		case '\\':
			append(&buffer, "\\\\")
		case:
			append(&buffer, value[i])
		}
	}
	return string(buffer[:])
}

run_command :: proc(command: string) {
	context = runtime.default_context()
	command_c := strings.clone_to_cstring(command)
	defer delete(command_c)
	_ = libc.system(command_c)
}

notify :: proc(title, message: string) {
	context = runtime.default_context()
	escaped_title := applescript_escape(title)
	escaped_message := applescript_escape(message)
	script := fmt.tprintf("display notification \"%s\" with title \"%s\" sound name \"Glass\"", escaped_message, escaped_title)
	run_command(fmt.tprintf("osascript -e %s", shell_escape(script)))
	say_command := fmt.tprintf("say %s >/dev/null 2>&1 &", shell_escape(message))
	run_command(say_command)
}

status_handler :: proc "c" (signum: posix.Signal) {
	context = runtime.default_context()
	_ = signum
	now := current_unix_time()
	remaining := int(target_time - now)

	message := ""
	if remaining <= 0 {
		message = "Der Timer ist bereits abgelaufen."
	} else if remaining < 60 {
		message = fmt.tprintf("Noch %d Sekunden.", remaining)
	} else {
		minutes := (remaining + 30) / 60
		unit := "Minuten"
		if minutes == 1 {
			unit = "Minute"
		}
		message = fmt.tprintf("Noch etwa %d %s.", minutes, unit)
	}

	notify("Timer Status", message)
}

detach_stdio :: proc() {
	context = runtime.default_context()
	null_path := strings.clone_to_cstring("/dev/null")
	defer delete(null_path)

	null_in := posix.open(null_path, {})
	if null_in != -1 {
		_ = posix.dup2(null_in, 0)
		_ = posix.close(null_in)
	}

	null_out := posix.open(null_path, { .WRONLY })
	if null_out != -1 {
		_ = posix.dup2(null_out, 1)
		_ = posix.dup2(null_out, 2)
		_ = posix.close(null_out)
	}
}

print_usage_error :: proc(message: string) {
	context = runtime.default_context()
	fmt.eprintf("%s%s%s\n", ANSI_BOLD_RED, message, ANSI_RESET)
	os.exit(1)
}

main :: proc() {
	context = runtime.default_context()
	when ODIN_OS != .Darwin {
		print_usage_error("Ich wecke nur unter macOS =:3")
	}

	ssh_tty := os.get_env_alloc("SSH_TTY", context.allocator)
	ssh_conn := os.get_env_alloc("SSH_CONNECTION", context.allocator)
	if ssh_tty != "" || ssh_conn != "" {
		print_usage_error("Ich wecke nicht remote!")
	}

	if len(os.args) < 2 {
		print_usage_error("Du musst schon sagen wann, z.B. '100 sek'.")
	}

	message, seconds, ok := parse_time(os.args[1:])
	if !ok {
		print_usage_error("Ich hab die Zeit nicht verstanden.")
	}

	target_time = current_unix_time() + cast(i64)seconds
	global_message = message

	pid := posix.fork()
	if pid == 0 {
		_ = posix.setsid()
		_ = posix.signal(.SIGUSR1, status_handler)
		detach_stdio()

		for {
			now := current_unix_time()
			if now >= target_time {
				break
			}

			remaining := target_time - now
			if remaining > 3600 {
				remaining = 3600
			}
			_ = posix.sleep(c.uint(remaining))
		}

		notify("Wecker", global_message)
		os.exit(0)
	}

	if pid < 0 {
		print_usage_error("Der Hintergrundprozess konnte nicht gestartet werden.")
	}

	fmt.printf("%s%s%s\n", ANSI_BOLD, message, ANSI_RESET)
	fmt.printf("%s%d Sekunden%s (läuft im Hintergrund)\n", ANSI_BOLD_GREEN, seconds, ANSI_RESET)
	fmt.printf("%sAbfrage: %s%skill -USR1 %d%s\n", ANSI_CYAN, ANSI_RESET, ANSI_BOLD, cast(int)pid, ANSI_RESET)
	fmt.printf("%sAbbruch: %s%skill %d%s\n", ANSI_RED, ANSI_RESET, ANSI_BOLD, cast(int)pid, ANSI_RESET)
	os.exit(0)
}