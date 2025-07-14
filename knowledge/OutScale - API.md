[[OutScale - API OpenTofu]]

Pour utiliser l'api de outscale, osc-cli il faut l'installer via python avec le tuto ici [Installer et configurer OSC CLI – Documentation publique OUTSCALE](https://docs.outscale.com/fr/userguide/Installer-et-configurer-OSC-CLI.html)

On peut avoir l'erreur suivante : 
### Erreur Python wheel
```
pip3 install osc-sdk
Defaulting to user installation because normal site-packages is not writeable
Collecting osc-sdk
  Using cached osc_sdk-1.11.0-py2.py3-none-any.whl.metadata (8.3 kB)
Requirement already satisfied: setuptools in /usr/lib/python3/dist-packages (from osc-sdk) (68.1.2)
Collecting defusedxml>=0.7.1 (from osc-sdk)
  Using cached defusedxml-0.7.1-py2.py3-none-any.whl.metadata (32 kB)
Collecting fire>=0.1.3 (from osc-sdk)
  Using cached fire-0.7.0.tar.gz (87 kB)
  Preparing metadata (setup.py) ... done
Requirement already satisfied: requests>=2.26.0 in /usr/lib/python3/dist-packages (from osc-sdk) (2.31.0)
Requirement already satisfied: typing-extensions>=3.10.0.2 in /usr/lib/python3/dist-packages (from osc-sdk) (4.10.0)
Requirement already satisfied: xmltodict>=0.11.0 in /usr/lib/python3/dist-packages (from osc-sdk) (0.13.0)
Collecting termcolor (from fire>=0.1.3->osc-sdk)
  Using cached termcolor-2.5.0-py3-none-any.whl.metadata (6.1 kB)
Using cached osc_sdk-1.11.0-py2.py3-none-any.whl (21 kB)
Using cached defusedxml-0.7.1-py2.py3-none-any.whl (25 kB)
Using cached termcolor-2.5.0-py3-none-any.whl (7.8 kB)
Building wheels for collected packages: fire
  Building wheel for fire (setup.py) ... error
  error: subprocess-exited-with-error
  
  × python setup.py bdist_wheel did not run successfully.
  │ exit code: 1
  ╰─> [149 lines of output]
      /usr/lib/python3/dist-packages/setuptools/_distutils/dist.py:265: UserWarning: Unknown distribution option: 'requires_python'
        warnings.warn(msg)
      running bdist_wheel
      running build
      running build_py
      creating build
      creating build/lib
      creating build/lib/fire
      copying fire/custom_descriptions_test.py -> build/lib/fire
      copying fire/decorators.py -> build/lib/fire
      copying fire/inspectutils_test.py -> build/lib/fire
      copying fire/docstrings_test.py -> build/lib/fire
      copying fire/test_components_test.py -> build/lib/fire
      copying fire/parser_test.py -> build/lib/fire
      copying fire/formatting.py -> build/lib/fire
      copying fire/test_components_bin.py -> build/lib/fire
      copying fire/core.py -> build/lib/fire
      copying fire/__init__.py -> build/lib/fire
      copying fire/helptext_test.py -> build/lib/fire
      copying fire/test_components_py3.py -> build/lib/fire
      copying fire/inspectutils.py -> build/lib/fire
      copying fire/docstrings.py -> build/lib/fire
      copying fire/core_test.py -> build/lib/fire
      copying fire/interact.py -> build/lib/fire
      copying fire/testutils.py -> build/lib/fire
      copying fire/fire_test.py -> build/lib/fire
      copying fire/value_types.py -> build/lib/fire
      copying fire/parser_fuzz_test.py -> build/lib/fire
      copying fire/docstrings_fuzz_test.py -> build/lib/fire
      copying fire/__main__.py -> build/lib/fire
      copying fire/main_test.py -> build/lib/fire
      copying fire/custom_descriptions.py -> build/lib/fire
      copying fire/formatting_test.py -> build/lib/fire
      copying fire/interact_test.py -> build/lib/fire
      copying fire/completion_test.py -> build/lib/fire
      copying fire/completion.py -> build/lib/fire
      copying fire/helptext.py -> build/lib/fire
      copying fire/trace_test.py -> build/lib/fire
      copying fire/test_components.py -> build/lib/fire
      copying fire/trace.py -> build/lib/fire
      copying fire/decorators_test.py -> build/lib/fire
      copying fire/fire_import_test.py -> build/lib/fire
      copying fire/formatting_windows.py -> build/lib/fire
      copying fire/testutils_test.py -> build/lib/fire
      copying fire/parser.py -> build/lib/fire
      creating build/lib/fire/console
      copying fire/console/text.py -> build/lib/fire/console
      copying fire/console/__init__.py -> build/lib/fire/console
      copying fire/console/console_attr_os.py -> build/lib/fire/console
      copying fire/console/console_attr.py -> build/lib/fire/console
      copying fire/console/console_io.py -> build/lib/fire/console
      copying fire/console/files.py -> build/lib/fire/console
      copying fire/console/platforms.py -> build/lib/fire/console
      copying fire/console/console_pager.py -> build/lib/fire/console
      copying fire/console/encoding.py -> build/lib/fire/console
      /usr/lib/python3/dist-packages/setuptools/_distutils/cmd.py:66: SetuptoolsDeprecationWarning: setup.py install is deprecated.
      !!
      
              ********************************************************************************
              Please avoid running ``setup.py`` directly.
              Instead, use pypa/build, pypa/installer or other
              standards-based tools.
      
              See https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html for details.
              ********************************************************************************
      
      !!
        self.initialize_options()
      installing to build/bdist.linux-x86_64/wheel
      running install
      running install_lib
      Traceback (most recent call last):
        File "<string>", line 2, in <module>
          exec(compile('''
          ~~~~^^^^^^^^^^^^
          # This is <pip-setuptools-caller> -- a caller that pip uses to run setup.py
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
          ...<31 lines>...
          exec(compile(setup_py_code, filename, "exec"))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
          ''' % ('/tmp/pip-install-korhokp8/fire_4fc37c89cde048d58473f8dfbbe6058a/setup.py',), "<pip-setuptools-caller>", "exec"))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File "<pip-setuptools-caller>", line 34, in <module>
        File "/tmp/pip-install-korhokp8/fire_4fc37c89cde048d58473f8dfbbe6058a/setup.py", line 43, in <module>
          setup(
          ~~~~~^
              name='fire',
              ^^^^^^^^^^^^
          ...<39 lines>...
              tests_require=TEST_DEPENDENCIES,
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
          )
          ^
        File "/usr/lib/python3/dist-packages/setuptools/__init__.py", line 107, in setup
          return distutils.core.setup(**attrs)
                 ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
        File "/usr/lib/python3/dist-packages/setuptools/_distutils/core.py", line 185, in setup
          return run_commands(dist)
        File "/usr/lib/python3/dist-packages/setuptools/_distutils/core.py", line 201, in run_commands
          dist.run_commands()
          ~~~~~~~~~~~~~~~~~^^
        File "/usr/lib/python3/dist-packages/setuptools/_distutils/dist.py", line 969, in run_commands
          self.run_command(cmd)
          ~~~~~~~~~~~~~~~~^^^^^
        File "/usr/lib/python3/dist-packages/setuptools/dist.py", line 1233, in run_command
          super().run_command(command)
          ~~~~~~~~~~~~~~~~~~~^^^^^^^^^
        File "/usr/lib/python3/dist-packages/setuptools/_distutils/dist.py", line 988, in run_command
          cmd_obj.run()
          ~~~~~~~~~~~^^
        File "/usr/lib/python3/dist-packages/wheel/bdist_wheel.py", line 403, in run
          self.run_command("install")
          ~~~~~~~~~~~~~~~~^^^^^^^^^^^
        File "/usr/lib/python3/dist-packages/setuptools/_distutils/cmd.py", line 318, in run_command
          self.distribution.run_command(command)
          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
        File "/usr/lib/python3/dist-packages/setuptools/dist.py", line 1233, in run_command
          super().run_command(command)
          ~~~~~~~~~~~~~~~~~~~^^^^^^^^^
        File "/usr/lib/python3/dist-packages/setuptools/_distutils/dist.py", line 988, in run_command
          cmd_obj.run()
          ~~~~~~~~~~~^^
        File "/usr/lib/python3/dist-packages/setuptools/command/install.py", line 78, in run
          return orig.install.run(self)
                 ~~~~~~~~~~~~~~~~^^^^^^
        File "/usr/lib/python3/dist-packages/setuptools/_distutils/command/install.py", line 708, in run
          self.run_command(cmd_name)
          ~~~~~~~~~~~~~~~~^^^^^^^^^^
        File "/usr/lib/python3/dist-packages/setuptools/_distutils/cmd.py", line 318, in run_command
          self.distribution.run_command(command)
          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
        File "/usr/lib/python3/dist-packages/setuptools/dist.py", line 1233, in run_command
          super().run_command(command)
          ~~~~~~~~~~~~~~~~~~~^^^^^^^^^
        File "/usr/lib/python3/dist-packages/setuptools/_distutils/dist.py", line 987, in run_command
          cmd_obj.ensure_finalized()
          ~~~~~~~~~~~~~~~~~~~~~~~~^^
        File "/usr/lib/python3/dist-packages/setuptools/_distutils/cmd.py", line 111, in ensure_finalized
          self.finalize_options()
          ~~~~~~~~~~~~~~~~~~~~~^^
        File "/usr/lib/python3/dist-packages/setuptools/command/install_lib.py", line 17, in finalize_options
          self.set_undefined_options('install',('install_layout','install_layout'))
          ~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File "/usr/lib/python3/dist-packages/setuptools/_distutils/cmd.py", line 296, in set_undefined_options
          setattr(self, dst_option, getattr(src_cmd_obj, src_option))
                                    ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
        File "/usr/lib/python3/dist-packages/setuptools/_distutils/cmd.py", line 107, in __getattr__
          raise AttributeError(attr)
      AttributeError: install_layout. Did you mean: 'install_platlib'?
      [end of output]
  
  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for fire
  Running setup.py clean for fire
Failed to build fire
ERROR: ERROR: Failed to build installable wheels for some pyproject.toml based projects (fire)
```

### Resolution
Pour résoudre cette erreur il suffit de faire : 
```
pip install --upgrade pip setuptools wheel
```