# Apache Kafka Setup (KRaft Mode)

Modern Kafka (3.3+ production-ready, 4.x KRaft-only) runs **without Zookeeper** using **KRaft** (Kafka Raft metadata mode). One process acts as both broker and controller, which is ideal for local learning.

**When do you need this?**

- **Course unit tests** (`mvn test`) use **`EmbeddedKafka`** (`spring-kafka-test`). You do **not** need a local Kafka for those.
- A **local Kafka broker** is needed for the **manual labs on Days 45-46** and for **Project 03 (PeopleHub)**.

Requires **Java 17+** (you will already have JDK 21; see `JAVA_AND_MAVEN_SETUP.md`). Default broker address: `localhost:9092`.

---

## 1. macOS

```bash
brew install kafka
kafka-topics --version
```

Homebrew installs scripts without the `.sh` suffix (`kafka-topics`, `kafka-console-producer`, ...) and a KRaft config. Locate it:

```bash
brew --prefix kafka          # e.g. /opt/homebrew/opt/kafka
ls "$(brew --prefix kafka)/libexec/config"   # look for server.properties (KRaft) or kraft/server.properties
```

### 1.1 Format storage (one time)

KRaft needs a cluster ID and formatted log directory before the first start.

```bash
KAFKA_CLUSTER_ID="$(kafka-storage random-uuid)"
echo "$KAFKA_CLUSTER_ID"

# Use the KRaft config that ships with your version:
CONFIG="$(brew --prefix kafka)/libexec/config/server.properties"
# On Kafka 3.x the file may be .../libexec/config/kraft/server.properties

kafka-storage format -t "$KAFKA_CLUSTER_ID" -c "$CONFIG"
```

If the config's `log.dirs` points at `/tmp/kraft-combined-logs`, data is lost on reboot; that is fine for labs. To persist, edit `log.dirs` to e.g. `/opt/homebrew/var/lib/kraft-combined-logs`, then format.

### 1.2 Start the broker

Run in a dedicated terminal (leave it open):

```bash
kafka-server-start "$CONFIG"
```

Or use the Homebrew service (if formatted with the config it uses):

```bash
brew services start kafka
brew services list
```

Stop with Ctrl+C, or `brew services stop kafka`.

---

## 2. Windows

Kafka's Windows scripts are not officially supported for production, so choose one of:

### Option A (recommended): WSL2 + Linux steps

1. In PowerShell (admin): `wsl --install -d Ubuntu`, restart if asked, create a Linux user.
2. In the Ubuntu shell install Java and download Kafka (section 3 below):

   ```bash
   sudo apt update && sudo apt install -y openjdk-21-jre-headless curl tar
   ```

3. Follow **section 3**. From Windows, `localhost:9092` is forwarded to WSL2 automatically, so your Spring app running on Windows can connect to `localhost:9092`.

### Option B: Native binary

1. Download the binary release (`kafka_2.13-<version>.tgz`) from <https://kafka.apache.org/downloads>.
2. Extract to a **short path without spaces**, e.g. `C:\kafka` (long paths break the Windows scripts).
3. In PowerShell (`JAVA_HOME` must be set):

   ```powershell
   cd C:\kafka
   .\bin\windows\kafka-storage.bat random-uuid
   .\bin\windows\kafka-storage.bat format -t <UUID_FROM_ABOVE> -c .\config\server.properties
   .\bin\windows\kafka-server-start.bat .\config\server.properties
   ```

   On Kafka 3.x use `.\config\kraft\server.properties`. Set `log.dirs=C:/kafka/data` in the config to avoid temp-folder cleanup.

   Scripts live in `bin\windows\` and end in `.bat`; substitute them for the commands in sections 4-5.

---

## 3. Linux / WSL2 / manual download (macOS too)

```bash
cd ~
curl -LO https://downloads.apache.org/kafka/<version>/kafka_2.13-<version>.tgz   # pick version from kafka.apache.org/downloads
tar -xzf kafka_2.13-<version>.tgz
cd kafka_2.13-<version>

KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
bin/kafka-storage.sh format -t "$KAFKA_CLUSTER_ID" -c config/server.properties   # 3.x: config/kraft/server.properties
bin/kafka-server-start.sh config/server.properties
```

Leave that terminal running. Use `bin/<tool>.sh` in place of the brew command names below.

---

## 4. Create a topic

In a **second** terminal (brew command names shown; add `.sh` and `bin/` for tarball installs):

```bash
kafka-topics --bootstrap-server localhost:9092 --create --topic course-smoke-test --partitions 3 --replication-factor 1
kafka-topics --bootstrap-server localhost:9092 --list
kafka-topics --bootstrap-server localhost:9092 --describe --topic course-smoke-test
```

Delete: `kafka-topics --bootstrap-server localhost:9092 --delete --topic course-smoke-test`.

## 5. Produce / consume smoke test

Terminal A (consumer):

```bash
kafka-console-consumer --bootstrap-server localhost:9092 --topic course-smoke-test --from-beginning
```

Terminal B (producer; type lines and press Enter):

```bash
kafka-console-producer --bootstrap-server localhost:9092 --topic course-smoke-test
> hello kafka
> second message
```

The consumer should print both messages. Optional: consumer groups with `--group lab-group`, and inspect with `kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group lab-group`.

Press Ctrl+C in each terminal to exit.

## 6. Spring Boot connection

Local manual runs use:

```yaml
spring:
  kafka:
    bootstrap-servers: localhost:9092
```

Put this in your `application-local.yml` (git-ignored) if the project template includes it. Tests override this with `EmbeddedKafka`.

---

## 7. Troubleshooting

| Symptom | Cause and fix |
|---------|---------------|
| `Connection to node -1 (localhost/127.0.0.1:9092) could not be established` / `Broker may not be available` | Broker is not running or still starting. Check the server terminal for errors; confirm with `lsof -i :9092` (macOS/Linux) or `netstat -ano \| findstr 9092` (Windows). |
| `Address already in use` on 9092 or 9093 | Another Kafka instance is running. Stop it (`brew services list`, `ps aux \| grep kafka`) or change `listeners` ports. 9093 is the KRaft controller port. |
| `No `meta.properties` found` / `Invalid cluster.id` / `log directory is not formatted` | Run `kafka-storage format` first. If you changed `log.dirs` or the cluster ID, delete the old log directory and format again. |
| `Inconsistent cluster ID` after reformat | Delete the old `log.dirs` folder (e.g. `/tmp/kraft-combined-logs`) before formatting again. |
| `process.roles` / `controller.quorum.voters` errors | You used a Zookeeper-era `server.properties`. Use the KRaft config shipped with your Kafka version. |
| `UnsupportedClassVersionError` / Java version errors | Kafka needs Java 17+. Check `java -version`. |
| Topics/data disappear after reboot | Default `log.dirs` is under `/tmp`. Set a persistent directory and re-format. |
| `Replication factor: 3 larger than available brokers: 1` | Local lab has a single broker. Use `--replication-factor 1`. |
| Spring app times out connecting from Windows to WSL2 Kafka | Make sure the broker's `advertised.listeners` is `PLAINTEXT://localhost:9092`, and restart WSL (`wsl --shutdown`) if localhost forwarding is stale. |
| Windows native: `The input line is too long` / path errors | Move Kafka to `C:\kafka` (short path, no spaces). |
| `mvn test` fails on Kafka tests | These should use `EmbeddedKafka` and not need a local broker. Check no stale process holds the random port, then run `mvn clean test`. Share the stack trace if it persists. |

Quick reset (labs only; **deletes all data**): stop the broker, delete the `log.dirs` directory, generate a new cluster ID, format, and start again.
