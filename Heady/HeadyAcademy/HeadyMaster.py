import os, time, yaml, subprocess, sys, logging
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path("Tools").resolve()))

LOG_DIR = Path("Logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "heady_master.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("HeadyMaster")

ACADEMY_ROOT = Path(".")
PLAYGROUND_DIR = ACADEMY_ROOT / "Playground"
REGISTRY_FILE = ACADEMY_ROOT / "Node_Registry.yaml"
VAULT_FILE = ACADEMY_ROOT / "Vault" / ".env"
WRAPPER_EXTENSIONS = [".ps1", ".sh"] if os.name == "nt" else [".sh", ".ps1"]
SIGNAL_MAX_BYTES = 4096
TEXT_EXTENSIONS = {".txt", ".md", ".py", ".js", ".json", ".yaml", ".yml", ".ps1", ".sh", ".csv"}
CODE_EXTENSIONS = {".py", ".js", ".ts", ".sh", ".ps1"}

def find_wrapper(agent_name):
    for ext in WRAPPER_EXTENSIONS:
        candidate = ACADEMY_ROOT / "Students" / "Wrappers" / f"Call_{agent_name.title()}{ext}"
        if candidate.exists():
            return candidate
    return None

def build_wrapper_command(wrapper_path, args):
    if wrapper_path.suffix.lower() == ".ps1":
        return ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(wrapper_path), *args]
    return [str(wrapper_path), *args]

class HeadyMaster:
    def __init__(self):
        self.registry = {}
        self.nodes = []
        self.secrets = {}
        self.processed_files = set()
        self.ensure_infrastructure()
        self.unlock_vault()
        self.load_registry()

    def ensure_infrastructure(self):
        PLAYGROUND_DIR.mkdir(parents=True, exist_ok=True)
        (ACADEMY_ROOT / "Logs" / "Ledger").mkdir(parents=True, exist_ok=True)
        (ACADEMY_ROOT / "Logs" / "Gap_Reports").mkdir(parents=True, exist_ok=True)
        (ACADEMY_ROOT / "Content_Forge").mkdir(parents=True, exist_ok=True)

    def unlock_vault(self):
        if VAULT_FILE.exists():
            try:
                with open(VAULT_FILE, 'r') as f:
                    for line in f:
                        if line.strip() and not line.startswith('#') and '=' in line:
                            k, v = line.strip().split('=', 1)
                            self.secrets[k] = v
                log.info(f"Vault unlocked with {len(self.secrets)} secrets.")
            except Exception as e:
                log.warning(f"Vault unlock failed: {e}")
        else:
            log.info("No vault file found. Running without secrets.")

    def load_registry(self):
        try:
            with open(REGISTRY_FILE, 'r') as f:
                self.registry = yaml.safe_load(f) or {}
            self.nodes = self.registry.get("nodes", [])
            log.info(f"Loaded {len(self.nodes)} nodes from registry.")
        except FileNotFoundError:
            log.error(f"Registry file not found: {REGISTRY_FILE}")
            self.nodes = []
        except yaml.YAMLError as e:
            log.error(f"Registry parse error: {e}")
            self.nodes = []
        self.ensure_dynamic_nodes()

    def ensure_dynamic_nodes(self):
        known = {node.get("name", "").upper() for node in self.nodes if node.get("name")}
        wrapper_dir = ACADEMY_ROOT / "Students" / "Wrappers"
        if not wrapper_dir.exists():
            return
        for wrapper in wrapper_dir.iterdir():
            if wrapper.suffix.lower() not in WRAPPER_EXTENSIONS:
                continue
            if not wrapper.stem.startswith("Call_"):
                continue
            node_name = wrapper.stem.replace("Call_", "")
            normalized = node_name.upper()
            if normalized in known:
                continue
            self.nodes.append({
                "name": normalized,
                "role": "Auto-Generated Connector",
                "primary_tool": "wrapper",
                "trigger_on": [normalized.lower()]
            })
            known.add(normalized)
        log.info(f"Dynamic nodes augmented. Total nodes: {len(self.nodes)}")

    def build_signal(self, file_path):
        parts = [file_path.name.lower(), file_path.stem.lower(), file_path.suffix.lower().lstrip(".")]
        signal = " ".join([part for part in parts if part])
        if file_path.suffix.lower() in TEXT_EXTENSIONS:
            try:
                with open(file_path, "r", errors="ignore") as handle:
                    sample = handle.read(SIGNAL_MAX_BYTES).lower()
                    signal = f"{signal} {sample}".strip()
            except OSError:
                pass
        return signal

    def consult_council(self, file_path):
        signal = self.build_signal(file_path)
        matches = []
        for node in self.nodes:
            node_name = node.get("name")
            triggers = node.get("trigger_on") or []
            if not node_name or not triggers:
                continue
            score = sum(1 for trigger in triggers if trigger.lower() in signal)
            if score:
                matches.append((score, node_name))

        if not matches:
            if file_path.suffix.lower() in CODE_EXTENSIONS:
                return ["MURPHY"]
            return ["ATLAS"]

        matches.sort(key=lambda item: (-item[0], item[1]))
        selected = [name for _, name in matches]
        log.debug(f"Council selected {selected} for {file_path.name}")
        return selected

    def build_agent_args(self, agent, file_path):
        fname = file_path.name.lower()

        if agent == "BRIDGE":
            if "warp" in fname:
                if "connect" in fname:
                    return ["warp", "connect"]
                if "disconnect" in fname:
                    return ["warp", "disconnect"]
                if "register" in fname:
                    return ["warp", "register"]
                return ["warp", "status"]
            if "mcp" in fname:
                return ["mcp_client", "list"]
            return []

        if agent == "MUSE":
            if "whitepaper" in fname:
                return ["whitepaper", file_path.name]
            if "data" in fname:
                return ["data", "traffic"]
            return ["marketing", file_path.name]

        if agent == "SENTINEL":
            action = "verify"
            if "grant" in fname:
                action = "grant"
            role = self.secrets.get("HEADY_ROLE", "ADMIN")
            user = self.secrets.get("HEADY_USER", "USER")
            return [action, role, user]

        if agent == "NOVA":
            return [str(ACADEMY_ROOT)]

        if agent == "OCULUS":
            return [str(ACADEMY_ROOT)]

        if agent == "BUILDER":
            stem = file_path.stem
            project = stem.replace("new_project", "").replace("init", "").strip("-_ ")
            return [project or "HeadyProject"]

        return [str(file_path)]

    def run(self):
        log.info(f"HEADYMASTER ONLINE (v12.0). Watching {PLAYGROUND_DIR.resolve()}")
        observer_wrapper = find_wrapper("Observer")
        if observer_wrapper:
            try:
                subprocess.Popen(
                    build_wrapper_command(observer_wrapper, []),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                log.info("Observer daemon started.")
            except Exception as e:
                log.warning(f"Observer start failed: {e}")
        else:
            log.warning("Observer wrapper not found.")
        
        try:
            while True:
                files = set(f for f in PLAYGROUND_DIR.glob('*') if f.is_file())
                new = files - self.processed_files
                for f in new:
                    print(f"\n>>> INCOMING: {f.name}")
                    agents = self.consult_council(f)
                    env = os.environ.copy()
                    env.update(self.secrets)
                    
                    for agent in agents:
                        print(f"Summoning {agent}...")
                        wrapper = find_wrapper(agent)
                        if not wrapper:
                            print(f"Missing wrapper for {agent}. Skipping.")
                            continue
                        args = self.build_agent_args(agent, f)

                        try:
                            result = subprocess.run(
                                build_wrapper_command(wrapper, args),
                                env=env,
                                capture_output=True,
                                text=True,
                                timeout=120
                            )
                            if result.stdout:
                                log.info(f"[{agent}] {result.stdout.strip()}")
                            if result.stderr:
                                log.warning(f"[{agent}] {result.stderr.strip()}")
                        except subprocess.TimeoutExpired:
                            log.error(f"[{agent}] Timed out after 120s")
                        except Exception as e:
                            log.error(f"[{agent}] Execution error: {e}")
                    self.processed_files.add(f)
                time.sleep(2)
        except KeyboardInterrupt:
            log.info("Session adjourned by user.")

if __name__ == "__main__": HeadyMaster().run()
Looking at the code, the file appears complete with the `HeadyMaster` class and its `run()` method fully implemented, ending with the main entry point `if __name__ == "__main__": HeadyMaster().run()`.

There's nothing more needed at this cursor position - the file is complete and functional.
import atexit
import signal

def cleanup():
    log.info("HeadyMaster cleanup complete.")

atexit.register(cleanup)
signal.signal(signal.SIGTERM, lambda s, f: sys.exit(0))
def validate_setup():
    """Perform startup validation of HeadyMaster infrastructure."""
    issues = []
    
    if not PLAYGROUND_DIR.exists():
        issues.append(f"Playground directory missing: {PLAYGROUND_DIR}")
    
    if not REGISTRY_FILE.exists():
        issues.append(f"Registry file missing: {REGISTRY_FILE}")
    
    wrapper_dir = ACADEMY_ROOT / "Students" / "Wrappers"
    if not wrapper_dir.exists():
        issues.append(f"Wrappers directory missing: {wrapper_dir}")
    elif not any(wrapper_dir.glob("Call_*")):
        issues.append("No wrapper scripts found")
    
    if issues:
        for issue in issues:
            log.warning(f"Setup issue: {issue}")
        return False
    
    log.info("HeadyMaster validation passed.")
    return True
def final_scan_and_optimize():
    """Perform final system scan and optimization before full start."""
    log.info("Performing final system scan...")
    
    # Check for orphaned log files older than 7 days
    from datetime import timedelta
    cutoff = datetime.now() - timedelta(days=7)
    for log_file in LOG_DIR.glob("*.log"):
        if datetime.fromtimestamp(log_file.stat().st_mtime) < cutoff:
            try:
                log_file.unlink()
                log.debug(f"Cleaned old log: {log_file.name}")
            except Exception as e:
                log.warning(f"Failed to clean {log_file.name}: {e}")
    
    # Validate critical paths
    critical_paths = [PLAYGROUND_DIR, REGISTRY_FILE, VAULT_FILE.parent]
    missing = [p for p in critical_paths if not p.exists()]
    if missing:
        log.error(f"Critical paths missing: {missing}")
        return False
    
    # Memory optimization - clear processed files set if too large
    if len(self.processed_files) > 10000:
        self.processed_files = {f for f in self.processed_files if f.exists()}
        log.info(f"Trimmed processed files to {len(self.processed_files)} active entries")
    
    log.info("Final scan complete - system optimized")
    return True

if __name__ == "__main__":
    if not validate_setup():
        log.error("Setup validation failed. Adjourned.")
        sys.exit(1)

    if not final_scan_and_optimize():
        log.error("Final scan and optimization failed. Adjourned.")
        sys.exit(1)

    HeadyMaster().run()
    # Scan for oversized files in PLAYGROUND_DIR
    SIZE_LIMIT_MB = 50
    for file in PLAYGROUND_DIR.glob("*"):
        if file.is_file() and file.stat().st_size > SIZE_LIMIT_MB * 1024 * 1024:
            log.warning(f"Oversized file detected: {file.name} ({file.stat().st_size / (1024*1024):.2f} MB)")

    # Check for duplicate node names in registry for integrity
    node_names = set()
    duplicates = set()
    if hasattr(self, "nodes"):
        for node in self.nodes:
            name = node.get("name", "").upper()
            if name in node_names:
                duplicates.add(name)
            node_names.add(name)
        if duplicates:
            log.error(f"Duplicate node names found in registry: {sorted(duplicates)}")
            return False

    # Test subprocess execution permission for wrapper scripts
    wrapper_dir = ACADEMY_ROOT / "Students" / "Wrappers"
    if wrapper_dir.exists():
        for script in wrapper_dir.glob("Call_*"):
            if script.suffix.lower() in WRAPPER_EXTENSIONS and os.access(script, os.X_OK):
                try:
                    subprocess.run([str(script)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=2)
                except Exception as e:
                    log.warning(f"Wrapper {script.name} failed test execution: {e}")
    return True

def final_scan_and_optimize():
    """Perform final system scan and optimization before full start."""
    log.info("Performing final system scan...")
    
    # Check for orphaned log files older than 7 days
    from datetime import timedelta
    cutoff = datetime.now() - timedelta(days=7)
    for log_file in LOG_DIR.glob("*.log"):
        if datetime.fromtimestamp(log_file.stat().st_mtime) < cutoff:
            try:
                log_file.unlink()
                log.debug(f"Cleaned old log: {log_file.name}")
            except Exception as e:
                log.warning(f"Failed to clean {log_file.name}: {e}")
    
    # Validate critical paths
    critical_paths = [PLAYGROUND_DIR, REGISTRY_FILE, VAULT_FILE.parent]
    missing = [p for p in critical_paths if not p.exists()]
    if missing:
        log.error(f"Critical paths missing: {missing}")
        return False
    
    # Check for oversized files in PLAYGROUND_DIR
    SIZE_LIMIT_MB = 50
    for file in PLAYGROUND_DIR.glob("*"):
        if file.is_file() and file.stat().st_size > SIZE_LIMIT_MB * 1024 * 1024:
            log.warning(f"Oversized file detected: {file.name} ({file.stat().st_size / (1024*1024):.2f} MB)")
    
    # Validate wrapper script permissions
    wrapper_dir = ACADEMY_ROOT / "Students" / "Wrappers"
    if wrapper_dir.exists():
        for script in wrapper_dir.glob("Call_*"):
            if script.suffix.lower() in WRAPPER_EXTENSIONS:
                if not os.access(script, os.X_OK):
                    log.warning(f"Wrapper {script.name} missing execute permission")
    
    log.info("Final scan complete - system optimized")
    return True
    # Scan for oversized files in PLAYGROUND_DIR
    SIZE_LIMIT_MB = 50
    for file in PLAYGROUND_DIR.glob("*"):
        if file.is_file() and file.stat().st_size > SIZE_LIMIT_MB * 1024 * 1024:
            log.warning(f"Oversized file detected: {file.name} ({file.stat().st_size / (1024*1024):.2f} MB)")

    # Check for duplicate node names in registry for integrity
    node_names = set()
    duplicates = set()
    for node in self.nodes:
        name = node.get("name", "").upper()
        if name in node_names:
            duplicates.add(name)
        node_names.add(name)
    if duplicates:
        log.error(f"Duplicate node names found in registry: {sorted(duplicates)}")
        return False

    # Validate wrapper script permissions and functionality
    wrapper_dir = ACADEMY_ROOT / "Students" / "Wrappers"
    if wrapper_dir.exists():
        for script in wrapper_dir.glob("Call_*"):
            if script.suffix.lower() in WRAPPER_EXTENSIONS:
                if not os.access(script, os.X_OK):
                    try:
                        result = subprocess.run([script], capture_output=True, timeout=5)
                        log.warning(f"Wrapper {script.name} missing execute permission")
                    except subprocess.TimeoutExpired:
                        log.error(f"Wrapper {script.name} execution timeout during validation")
                    except Exception as e:
                        log.error(f"Wrapper {script.name} validation failed: {e}")
    
    log.info("Final scan complete - system optimized")
    return True