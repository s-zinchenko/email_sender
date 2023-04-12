#!/bin/bash

NAME="email_sender"                                  							              # Name of the application
DJANGODIR=/app/email_sender             				        # Django project directory
DJANGOENVDIR=/app/email_sender/venv            			    # Django project env
SOCKFILE=/app/email_sender/run/gunicorn.sock  		  # we will communicte using this unix socket
USER=root                                        					              # the user to run as
GROUP=root                                     							            # the group to run as
NUM_WORKERS=3                                    							            # how many worker processes should Gunicorn spawn (2 * CPUs + 1)
DJANGO_SETTINGS_MODULE=email_sender.settings             						            # which settings file should Django use
DJANGO_WSGI_MODULE=email_sender.wsgi                     						            # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /app/email_sender/venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ${DJANGOENVDIR}/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-