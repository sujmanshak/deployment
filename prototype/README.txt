The enclosed files are a prototype of a remote VoltDB deployment daemon (voltrc) 
and shell command to invoke the daemon (voltd).

The daemon starts a small web server that responds to REST-like commands as well as 
offering a web interface (unfinished). To use the daemon, you must add bootstrap 
and font-awesome to the assets subfolder.

Use voltrc/nohupvoltrc.sh to start the daemon as a detached process.

Use python voltd.py as the command line to invoke the remote daemon.