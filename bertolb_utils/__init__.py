def format_location(raw_location):
    if raw_location.endswith('/'):
        return raw_location
    else:
        return raw_location + '/'


def build_ssh_command(hostname, username, pkey_path, port=22, extra_args=None,
                      tunnel=False, tunnel_port=8157,
                      bastion=False, bastion_hostname=None, bastion_username=None, bastion_port=22):
    # TODO rework this crap
    start = 'ssh'
    default_options = '-o StrictHostKeyChecking=no -o ServerAliveInterval=10'
    bastion_options = '-At'
    tunnel_flag = '-ND'
    key_flag = '-i'

    command = [start]

    if bastion:
        command.append(bastion_options)
    command.append(default_options)
    if tunnel:
        command += [tunnel_flag, str(tunnel_port)]
    command += [key_flag, pkey_path]
    if bastion:
        command += [bastion_username + '@' + bastion_hostname, '-p', str(bastion_port), start, default_options]
    command += [username + '@' + hostname, '-p', str(port)]
    if extra_args:
        command.append(extra_args)

    return ' '.join(command)
