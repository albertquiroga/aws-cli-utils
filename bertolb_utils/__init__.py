def format_location(raw_location):
    if raw_location.endswith('/'):
        return raw_location
    else:
        return raw_location + '/'


def _combine_ssh_args(hostname, username, key_path=None, port=22, ssh_options='', extra_args=''):
    import re
    command = "ssh %s %s %s@%s -p %i %s"%(ssh_options, "-i " + key_path if key_path else '', username, hostname, port, extra_args)
    return re.sub(' +', ' ', command.strip())  # Remove leading/trailing spaces plus double spaces in the middle


def build_ssh_command(hostname, username, pkey_path, port=22, ssh_options='', extra_args='',
                      tunnel=False, tunnel_port=8157,
                      bastion=False, bastion_hostname='', bastion_username='', bastion_pkey_path='', bastion_port=22):
    res = _combine_ssh_args(hostname, username, pkey_path, port, ssh_options, extra_args)

    if bastion:
        return _combine_ssh_args(bastion_hostname, bastion_username, bastion_pkey_path, bastion_port, ssh_options='-At -o StrictHostKeyChecking=no -o ServerAliveInterval=10', extra_args=res)
    elif tunnel:
        return res + ' -ND ' + str(tunnel_port)
    else:
        return res
