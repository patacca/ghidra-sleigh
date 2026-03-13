project(
  'ghidra-sleigh',
  'cpp',
  version: run_command('python3', 'scripts/get_ghidra_info.py', 'version', check: false).stdout().strip(),
  license: 'Apache-2.0',
  meson_version: '>= 1.6',
  default_options: [
    'cpp_std=c++11',
    'buildtype=release',
    'warning_level=0',
  ],
)

# ---------------------------------------------------------------------------
# Derive Ghidra metadata from the git submodule.
# The helper script reads `git describe --tags --exact-match` and
# `git rev-parse HEAD` inside third_party/ghidra and falls back gracefully
# when git is unavailable or the submodule is not at an exact tag.
# ---------------------------------------------------------------------------
_info_script = files('scripts/get_ghidra_info.py')

ghidra_tag    = run_command('python3', _info_script, 'tag',    check: false).stdout().strip()
ghidra_commit = run_command('python3', _info_script, 'commit', check: false).stdout().strip()

meson.add_dist_script(files('scripts/dist_ghidra.py'))

py = import('python').find_installation(pure: true)

# ---------------------------------------------------------------------------
# Path to the Ghidra upstream source tree.
# Defaults to the bundled git submodule at third_party/ghidra.
# Override with -Dghidra_root=/path/to/ghidra if you have an existing checkout.
# ---------------------------------------------------------------------------
ghidra_root = get_option('ghidra_root')
# Source-relative path for source files and include_directories (Meson
# resolves these against meson.current_source_dir() automatically).
ghidra_src = ghidra_root / 'Ghidra' / 'Features' / 'Decompiler' / 'src' / 'decompile' / 'cpp'

# Absolute path for custom_target commands that run from the build directory.
fs = import('fs')
if fs.is_absolute(ghidra_root)
  ghidra_root_abs = ghidra_root
else
  ghidra_root_abs = meson.current_source_dir() / ghidra_root
endif
processors_root = ghidra_root_abs / 'Ghidra' / 'Processors'

ghidra_inc = include_directories(ghidra_src)
zlib_dep = dependency('zlib')

# ---------------------------------------------------------------------------
# sleighc -- the Sleigh specification compiler
# Sources: CORE + SLEIGH + SLACOMP (from upstream Makefile)
# ---------------------------------------------------------------------------
sleighc_sources = [
  # CORE
  ghidra_src / 'xml.cc',
  ghidra_src / 'marshal.cc',
  ghidra_src / 'space.cc',
  ghidra_src / 'float.cc',
  ghidra_src / 'address.cc',
  ghidra_src / 'pcoderaw.cc',
  ghidra_src / 'translate.cc',
  ghidra_src / 'opcodes.cc',
  ghidra_src / 'globalcontext.cc',
  # SLEIGH
  ghidra_src / 'sleigh.cc',
  ghidra_src / 'pcodeparse.cc',
  ghidra_src / 'pcodecompile.cc',
  ghidra_src / 'sleighbase.cc',
  ghidra_src / 'slghsymbol.cc',
  ghidra_src / 'slghpatexpress.cc',
  ghidra_src / 'slghpattern.cc',
  ghidra_src / 'semantics.cc',
  ghidra_src / 'context.cc',
  ghidra_src / 'slaformat.cc',
  ghidra_src / 'compression.cc',
  ghidra_src / 'filemanage.cc',
  # SLACOMP (the compiler itself; contains main())
  ghidra_src / 'slgh_compile.cc',
  ghidra_src / 'slghparse.cc',
  ghidra_src / 'slghscan.cc',
]

sleighc_exe = executable(
  'sleighc',
  sleighc_sources,
  include_directories: ghidra_inc,
  dependencies: zlib_dep,
  native: true,
)

# ---------------------------------------------------------------------------
# Compile .sla files for each processor.
# sleighc -a <processor_dir> compiles all .slaspec files recursively.
#
# By default all Ghidra-supported processors are compiled (~26 MB installed).
# Set -Dall_processors=false to compile only the major ISAs (~10 MB).
# ---------------------------------------------------------------------------
python_prog = find_program('python3', 'python')
sleigh_compile_script = files('scripts' / 'sleigh_compile.py')

# DATA is required by other processors for shared cspec files.
priority_processors = ['DATA', 'x86', 'AARCH64', 'RISCV', 'MIPS']

all_processors_opt = get_option('all_processors')

if all_processors_opt
  # Discover all processor directories at configure time
  proc_scan = run_command(
    python_prog,
    '-c',
    'import os, sys; root = sys.argv[1]; dirs = sorted(d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))); print("\\n".join(dirs))',
    processors_root,
    check: true,
  )
  processors = proc_scan.stdout().strip().split('\n')
else
  processors = priority_processors
endif

sleigh_stamps = []
foreach proc : processors
  proc = proc.strip()
  if proc == ''
    continue
  endif
  stamp = custom_target(
    'sleigh-' + proc,
    command: [python_prog, sleigh_compile_script, sleighc_exe, processors_root / proc, '@OUTPUT@'],
    output: 'sleigh-' + proc + '.stamp',
    build_by_default: true,
  )
  sleigh_stamps += stamp
endforeach

# ---------------------------------------------------------------------------
# Install runtime data files (.sla, .ldefs, .pspec, .cspec) into the
# Python package data directory.
#
# Installed layout (relative to site-packages):
#   ghidra_sleigh/data/Ghidra/Processors/<PROC>/data/languages/<files>
#
# This matches the directory structure that SleighArchitecture::
# scanForSleighDirectories() expects when given the .../data path as root.
# ---------------------------------------------------------------------------
foreach proc : processors
  proc = proc.strip()
  if proc == ''
    continue
  endif
  install_subdir(
    processors_root / proc / 'data' / 'languages',
    install_dir: py.get_install_dir() / 'ghidra_sleigh' / 'data' / 'Ghidra' / 'Processors' / proc / 'data',
    exclude_files: [],
  )
endforeach

subdir('src' / 'ghidra_sleigh')
