_version_conf = configuration_data()
_version_conf.set('VERSION',       meson.project_version())
_version_conf.set('GHIDRA_TAG',    ghidra_tag)
_version_conf.set('GHIDRA_COMMIT', ghidra_commit)
_version_conf.set('PROCESSORS',    '"' + '", "'.join(processors) + '",')


_version_py = configure_file(
  input:         '_version.py.in',
  output:        '_version.py',
  configuration: _version_conf,
)

py.install_sources(
  '__init__.py',
  'py.typed',
  _version_py,
  subdir: 'ghidra_sleigh',
)
