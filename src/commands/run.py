from pathlib import Path

current_dir = Path(__file__).resolve().parent
sio2path = current_dir.parent.parent / "bin" / "sio2jail"

def prep_command(tl, ml, e):
    command = (f'{sio2path}'
        ' --mount-namespace off'
        ' --pid-namespace off'
        ' --uts-namespace off'
        ' --ipc-namespace off'
        ' --net-namespace off'
        ' --capability-drop off'
        ' --user-namespace off'
        f' --instruction-count-limit {int(2 * tl)}M'
        f' --rtimelimit {int(16 * tl + 1000)}ms'
        f' --memory-limit {int(ml)}K'
        ' --output-limit 51200K'
        ' --output oiaug'
        f' -- {e}'
    )
    return command

print(prep_command(2, 10000, "a.out < test.in"))