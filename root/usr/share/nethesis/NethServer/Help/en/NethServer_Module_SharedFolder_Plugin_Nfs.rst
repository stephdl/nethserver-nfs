.. --initial-header-level=3 

Nfs
^^^
Network File System (NFS)


Enable NFS
    Enable the Nfs acces for this share

Allow in read-only on your LAN
    Quick Option to allow this share to all clients 
    of your local network in a Read Only mode

Allowed IP client list
    List all allowed IP to this share (one per line)

Allow write Access
    Allow write access to the IP client list. 

Use the server UID/GID Ownership
    Use the linux acl permissions. To read or write to the share, 
    the users of the remote nfs client must belong of the owner
    group GID. Otherwise if this option is not set, the gid is overstepped, 
    this makes the share less secure but easier to set up.

Prohibit the root power
    You can forbid the power of all roots to this share, 
    root can overstep the remote GID

Create a new gid/group on the remote client
    groupadd -g GidNumber -o GroupName

Add a secondary group to a user on the remote client
    usermod -a -G GidNumber UserName
