import sublime
import sublime_plugin
import os
import subprocess

class CompileWithGccCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        file_path = self.view.file_name()

        if not file_path:
            sublime.message_dialog("Save file.")
            return

        if not file_path.endswith(".c"):
            sublime.message_dialog("Only .c files.")
            return

        file_dir = os.path.dirname(file_path)
        output_exe = os.path.join(file_dir, "a.out")

        compile_command = ["gcc", file_path, "-o", output_exe]

        try:
            result = subprocess.run(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=file_dir, text=True)

            if result.returncode != 0:
                self.show_output(result.stderr)
                return

            run_command = f"\"{output_exe}\"; echo; echo '--- Finished ---'; exec bash"
            subprocess.Popen(["xterm", "-hold", "-e", f"bash -c '{run_command}'"], cwd=file_dir)

        except Exception as e:
            sublime.message_dialog("Error: " + str(e))

    def show_output(self, content):
        output_view = self.view.window().new_file()
        output_view.set_name("GCC Errors")
        output_view.set_scratch(True)
        output_view.run_command("append", {"characters": content})
