TODO
====

Bugs
----

* When executing the "clear" shell command, the new screen has a newline at the
  top

* Error when generating a config::

    $ make generate-config
    rm -rf ~/.dreamssh/config.ini
    python -c "from dreamssh import config; config.writeDefaults();"
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
      AttributeError: 'module' object has no attribute 'writeDefaults'
      make: *** [generate-config] Error 1

Tasks
-----

* Split out SSH Server code into a separate project?
  * make dreammud use it
  * make inversum use it

* Add support for shared sessions
  * we want to be able to provide a shell where everyone that logs in sees what
    everyone else is doing
  * this can be prototyped in the sandbox
  * this should be as easy as setting up a singleton session...

* Update SSH server to accept keys from non-~/.ssh dirs
  * store keys in configured dir
  * maybe subdirs, divided by user?

* Maybe move commandAPI from shell.base.MOTDColoredManhole to
  CarapiceInterpreter?

* Add support for dynamic prompts

* Add support for a status bar on the screen somewhere

* Remove os and sys calls that aren't safe
  * maybe follow Google App Engine's lead on this one?

* Add generic support for roles
  * provide a mechanism whereby programmers can create roles, and
  * assign different APIs or limited APIs to roles

* Add phased login
  * a login to create an account
  * provide a user name
  * provide a URL for SSH keys
  * keep a global cache of ssh keys and don't allow new user-creation if ssh
    keys are already present
  * allow for this code to be extendable
  * if anonymous, do phase 1 login
  * if not anonymous, do a full login
  * provide for the ability to define what the anonymous user name is
    * make the default anonymous user "signup"
