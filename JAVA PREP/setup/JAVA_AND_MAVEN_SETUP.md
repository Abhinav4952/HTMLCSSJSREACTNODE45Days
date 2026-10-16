# Java 21 and Maven Setup

This course requires **JDK 21 (LTS)** and **Apache Maven 3.9+**. We recommend the **Eclipse Temurin** JDK build and **IntelliJ IDEA Community Edition**.

Target result: both commands work in a fresh terminal.

```bash
java -version    # openjdk version "21.x.x" ... Temurin-21
mvn -version     # Apache Maven 3.9.x ... Java version: 21.x.x
```

---

## 1. macOS

### 1.1 Install Homebrew (if missing)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew --version
```

On Apple Silicon, follow the installer's "Next steps" to add `/opt/homebrew/bin` to your `PATH`.

### 1.2 Install JDK 21 and Maven

**Option A — Homebrew OpenJDK 21 (no admin password):**

```bash
brew install openjdk@21 maven
sudo ln -sfn /opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk \
  /Library/Java/JavaVirtualMachines/openjdk-21.jdk   # optional system symlink
export JAVA_HOME="/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home"
export PATH="$JAVA_HOME/bin:$PATH"
```

**Option B — Temurin 21 cask (may prompt for your macOS password):**

```bash
brew install --cask temurin@21
brew install maven
```

### 1.3 Set `JAVA_HOME` (zsh, the default macOS shell)

macOS ships a helper that finds installed JDKs:

```bash
# Homebrew OpenJDK 21 (Option A):
export JAVA_HOME="/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home"

# Or Temurin / any JDK registered with macOS:
/usr/libexec/java_home -v 21
# export JAVA_HOME="$(/usr/libexec/java_home -v 21)"
```

Add to `~/.zshrc` (prefer the Homebrew path if you used Option A):

```bash
# Option A (Homebrew openjdk@21):
export JAVA_HOME="/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home"
# Option B (Temurin / system-registered JDK 21):
# export JAVA_HOME="$(/usr/libexec/java_home -v 21)"
export PATH="$JAVA_HOME/bin:$PATH"
```

Reload and verify:

```bash
source ~/.zshrc
echo "$JAVA_HOME"
java -version
mvn -version
```

> Brew-installed Maven uses whichever JDK `JAVA_HOME` points to. If `mvn -version` shows a different Java than 21, fix `JAVA_HOME` first.

### 1.4 Multiple JDKs

List all: `/usr/libexec/java_home -V`. Switch per shell with `export JAVA_HOME="$(/usr/libexec/java_home -v 21)"`.

---

## 2. Windows 10/11

### 2.1 Install Temurin 21

**Option A: winget (recommended)**

Open PowerShell:

```powershell
winget install EclipseAdoptium.Temurin.21.JDK
```

**Option B: Adoptium installer**

1. Go to <https://adoptium.net/temurin/releases/?version=21>.
2. Choose OS **Windows**, architecture **x64** (or **aarch64** on ARM), package type **JDK**, and download the `.msi`.
3. Run the installer. On the "Custom Setup" page, enable **Set JAVA_HOME variable** and **Add to PATH**.

### 2.2 Install Maven

**Option A: Chocolatey**

```powershell
choco install maven
```

**Option B: Scoop**

```powershell
scoop install maven
```

**Option C: Manual download**

1. Download the binary zip from <https://maven.apache.org/download.cgi> (`apache-maven-3.9.x-bin.zip`).
2. Extract to `C:\Program Files\Apache\maven` (so `bin\mvn.cmd` is at `C:\Program Files\Apache\maven\bin\mvn.cmd`).
3. Add `C:\Program Files\Apache\maven\bin` to the `Path` (see below).

### 2.3 Set `JAVA_HOME` and `Path`

If the Adoptium installer did not set them:

1. Press Start, search **Edit the system environment variables**, click **Environment Variables...**.
2. Under **User variables** click **New...**
   - Name: `JAVA_HOME`
   - Value: `C:\Program Files\Eclipse Adoptium\jdk-21.0.x.x-hotspot` (check the actual folder name in Explorer)
3. Edit `Path` and add `%JAVA_HOME%\bin` (and the Maven `bin` folder if installed manually).
4. Click OK on all dialogs and **open a new terminal**.

Or via PowerShell (adjust the path):

```powershell
setx JAVA_HOME "C:\Program Files\Eclipse Adoptium\jdk-21.0.5.11-hotspot"
```

Verify in a **new** PowerShell window:

```powershell
echo $env:JAVA_HOME
java -version
mvn -version
```

---

## 3. IntelliJ IDEA Community

1. Download from <https://www.jetbrains.com/idea/download/> (choose **Community**), or:
   - macOS: `brew install --cask intellij-idea-ce`
   - Windows: `winget install JetBrains.IntelliJIDEA.Community`
2. Launch IntelliJ. Optional but useful plugins (Settings → Plugins): none are required; Maven support is bundled.
3. **Open a task as a Maven project:**
   - File → **Open...** and select the task folder (the one containing `pom.xml`), e.g. `Day 01/practical-tasks/task-01-.../`.
   - Choose **Open as Project** and **Trust Project**.
   - If a "Maven project needs to be imported" balloon appears, click **Load Maven Project**. Otherwise right-click `pom.xml` → **Add as Maven Project**.
4. **Set the Project SDK to JDK 21:**
   - File → **Project Structure...** (⌘; on macOS, Ctrl+Alt+Shift+S on Windows) → **Project**.
   - **SDK:** pick Temurin 21. If missing: **Add SDK → Download JDK...** → Version 21, Vendor Eclipse Temurin (or **Add SDK → JDK...** and select the installed path).
   - **Language level:** `21`.
5. **Maven JDK for imports:** Settings → Build, Execution, Deployment → Build Tools → Maven → **Runner** → JRE: **Use Project JDK**. Under **Importing**, set "JDK for importer" to **Use Project JDK**.
6. **Maven home:** same Maven settings page → "Maven home path": **Bundled** is fine, or point to your brew/manual install so IDE and terminal match.
7. **Run tests:** open a test class and click the green gutter icon, or open the Maven tool window → Lifecycle → `test`.

Tip: open one task folder at a time (or a day folder with each `pom.xml` added as a Maven project) to keep indexing fast.

---

## 4. Troubleshooting

| Symptom | Likely cause and fix |
|---------|----------------------|
| `java: command not found` / `'java' is not recognized` | JDK not on `PATH`. Reinstall or add `$JAVA_HOME/bin` (`%JAVA_HOME%\bin` on Windows). Open a **new** terminal. |
| `java -version` shows 8, 11, or 17 | Another JDK earlier in `PATH`. macOS: set `JAVA_HOME` via `/usr/libexec/java_home -v 21`. Windows: move `%JAVA_HOME%\bin` above other Java entries. Check with `which -a java` / `where java`. |
| `mvn -version` shows wrong Java | Maven uses `JAVA_HOME`. Fix `JAVA_HOME`, open a new terminal. |
| `The JAVA_HOME environment variable is not defined correctly` | `JAVA_HOME` points at the `bin` folder or a missing path. It must point at the JDK root (the folder containing `bin`, `lib`). No trailing `\bin`. |
| `Fatal error compiling: error: release version 21 not supported` | Maven is running on an older JDK. Fix `JAVA_HOME`; in IntelliJ set Maven Runner JRE to Project JDK 21. |
| `invalid target release: 21` | Same as above. |
| `mvn: command not found` | Maven not on `PATH`. `brew install maven`, or add Maven's `bin` folder on Windows and open a new terminal. |
| Dependencies fail to download (`PKIX path building failed`, `Could not transfer artifact`) | Corporate proxy/VPN or TLS inspection. Try off-VPN; configure `~/.m2/settings.xml` with your proxy; or import the corporate CA into the JDK truststore. |
| Dependency download from a private mirror fails | Check `~/.m2/settings.xml` for a `<mirror>` entry pointing at an internal repo; temporarily comment it out to use Maven Central. |
| Corrupted local repo (`.lastUpdated` files, "invalid LOC header") | Delete the affected folder under `~/.m2/repository/...` and re-run `mvn test`, or run `mvn -U clean test`. |
| IntelliJ red imports after opening | Maven tool window → Reload All Maven Projects; File → Invalidate Caches / Restart. |
| IntelliJ "Cannot resolve symbol" for Java 21 features | Project SDK or language level is below 21 (Project Structure → Project and Modules). |
| Tests pass in IDE but fail in terminal (or vice versa) | IDE and CLI use different JDKs. Align them as described above and run `mvn clean test`. |
| Windows: `'mvn' is not recognized` after manual install | Path entry typo or terminal not restarted. Run `where mvn` in a new terminal. |
| Apple Silicon: x64 JDK installed | Prefer the native aarch64 build; `brew install --cask temurin@21` installs the correct one. |

If still stuck, share the output of `java -version`, `mvn -version`, and `echo $JAVA_HOME` (`echo $env:JAVA_HOME` on PowerShell) with your instructor.
