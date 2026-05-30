#  Distributed Search Engine using Apache Hadoop

> A distributed search engine built with Apache Hadoop (HDFS + MapReduce) that processes large-scale text datasets, builds an inverted index, and enables fast keyword-based document retrieval across a multi-node cluster.

---

##  Group Members

| Roll Number | 
|-------------|
| 25K-8016    |
| 25K-8027    |

**Course:** Big Data Analytics  
**University:** FAST NUCES, Karachi Campus  

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Dataset](#dataset)
- [Cluster Configuration](#cluster-configuration)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [How to Run](#how-to-run)
- [Search Interface](#search-interface)
- [Web UI](#web-ui)
- [Technologies Used](#technologies-used)

---

## Overview

With the rapid growth of digital content, retrieving relevant information from large unstructured text collections is a major challenge. This project addresses this by building a **distributed search engine** using Apache Hadoop on a 2-node Windows cluster.

The system:
- Stores ~300 text documents (~700 MB) in **HDFS** distributed across 2 nodes
- Builds an **inverted index** using **MapReduce** (Python streaming)
- Enables **keyword-based search** returning matching documents with frequency counts
- Provides a **Flask web UI** for interactive querying

---

## Features

1. Distributed storage across master and slave nodes via HDFS
2. Parallel inverted index construction using MapReduce
3. Stopword filtering and text preprocessing in the mapper
4. Word frequency counting per document in the reducer
5. Fast keyword search via HDFS CLI or Flask web app
6. Real-time cluster monitoring via YARN and HDFS web UIs

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   User Query                        │
│              (Flask UI / HDFS CLI)                  │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│              Inverted Index (HDFS)                  │
│         word → doc1(freq), doc2(freq), ...          │
└────────────────────┬────────────────────────────────┘
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
┌─────────────────┐   ┌─────────────────┐
│   Map Phase     │   │  Reduce Phase   │
│  (mapper2.py)   │   │ (reducer2.py)   │
│                 │   │                 │
│ word → docID   │   │ word → docID(n) │
└────────┬────────┘   └────────┬────────┘
         │                     │
         └──────────┬──────────┘
                    ▼
┌─────────────────────────────────────────────────────┐
│              HDFS Input (~700 MB)                   │
│           /searchengine1/input/*.txt                │
│    Distributed across Master + Slave DataNodes      │
└─────────────────────────────────────────────────────┘
```

---

##  Dataset

| Property | Details |
|----------|---------|
| Total Documents | ~300 text files |
| Total Size | ~700 MB |
| Format | Unstructured plain text (.txt) |
| Naming | doc1.txt, doc2.txt, ..., doc300.txt |
| HDFS Path | `/searchengine1/input/` |
| Replication Factor | 2 (stored on both nodes) |

The dataset consists of synthetically generated text documents covering topics in distributed computing, big data, and information retrieval; designed to validate distributed indexing at scale.

---

## Cluster Configuration

| Parameter | Master Node | Slave Node |
|-----------|-------------|------------|
| Role | NameNode + ResourceManager | DataNode + NodeManager |
| IP Address | 25.30.131.240 | 25.30.135.182 |
| HDFS UI | http://25.30.131.240:9870 | http://25.30.131.240:9870 |
| YARN UI | http://25.30.131.240:8088 | http://25.30.131.240:8088 |
| OS | Windows 11 | Windows 11 |
| Hadoop Version | 3.3.1 | 3.3.1 |

---

## Project Structure

```
distributed-search-engine/
│
├── mapper2.py              # MapReduce Mapper — tokenizes text, emits (word, docID)
├── reducer2.py             # MapReduce Reducer — aggregates to inverted index
├── app.py                  # Flask web application for search UI
│
├── templates/
│   └── index.html          # Search UI frontend (HTML + CSS)
│
├── documents/              # Sample input text documents
│   ├── doc1.txt
│   ├── doc2.txt
│   └── ...
│
└── README.md
```

---

## Setup and Installation

### Prerequisites

- Apache Hadoop 3.3.1 installed on both nodes
- Java JDK 8 installed
- Python 3.10 installed
- Both nodes connected over VPN
- Flask installed: `pip install flask`

### 1. Start the Hadoop Cluster (on Master)

```cmd
start-dfs.cmd
start-yarn.cmd
```

Verify both nodes are live:
```cmd
jps
```

### 2. Create HDFS Input Directory

```cmd
hdfs dfs -mkdir -p /searchengine1/input
```

### 3. Upload Documents to HDFS

```cmd
hdfs dfs -put C:\Users\Mutaal\Desktop\Documents\* /searchengine1/input/
```

Verify upload:
```cmd
hdfs dfs -ls /searchengine1/input/
```

---

## How to Run

### Step 1 — Navigate to project folder

```cmd
cd C:\Users\Mutaal\Desktop\Documents
```

### Step 2 — Delete old output (if re-running)

```cmd
hdfs dfs -rm -r /searchengine1/output
```

### Step 3 — Run the MapReduce Job

```cmd
hadoop jar %HADOOP_HOME%/share/hadoop/tools/lib/hadoop-streaming-3.3.1.jar -files "mapper2.py,reducer2.py" -mapper "python mapper2.py" -reducer "python reducer2.py" -input /searchengine1/input -output /searchengine1/output
```

You will see progress like:
```
map 0% reduce 0%
map 50% reduce 0%
map 100% reduce 100%
```

### Step 4 — Verify the Inverted Index

```cmd
hdfs dfs -ls /searchengine1/output/
hdfs dfs -cat /searchengine1/output/part-00000
```

Sample output:
```
distributed     doc2(2), doc45(3), doc98(1), doc150(2)
hadoop          doc1(31), doc2(20), doc3(21), doc45(1), doc77(585)
mapreduce       doc12(4), doc67(2), doc188(1)
```

---

##  Search Interface

### Command Line Search (No Python required)

```cmd
hdfs dfs -cat /searchengine1/output/part-00000 | findstr /i "hadoop"
```

Replace `hadoop` with any keyword.


---

## Web UI

A Flask-based web interface is included for interactive search.

### Run the Web App

```cmd
cd C:\Users\Mutaal\Desktop\Documents
python app.py
```

Open your browser and go to:
```
http://localhost:5000
```

### Features
- Search bar with keyword input
- Live results showing matching documents and hit counts
- Cluster statistics display (documents, dataset size, index entries, nodes, map tasks)
- Relevance bar showing relative keyword frequency per document

## Technologies Used

| Technology | Version | Purpose |
|------------|---------|---------|
| Apache Hadoop HDFS | 3.3.1 | Distributed file storage |
| Apache Hadoop MapReduce | 3.3.1 | Parallel inverted index construction |
| Apache YARN | 3.3.1 | Resource management and job scheduling |
| Hadoop Streaming | 3.3.1 | Python script integration with MapReduce |
| Python | 3.10 | Mapper, reducer, search script, Flask app |
| Flask | Latest | Web-based search UI |
| Windows | 11 | Host OS for both cluster nodes |

---

## Monitoring

- **HDFS NameNode UI:** http://25.30.131.240:9870      (Replace this according to your IP Address) 
- **YARN Resource Manager:** http://25.30.131.240:8088 (Replace this according to your IP Address) 

---

## Notes

- Always run `start-dfs.cmd` and `start-yarn.cmd` before submitting any MapReduce job
- Restart the slave DataNode if it goes offline: run `hdfs --daemon start datanode` on the slave machine
- The `mapred-site.xml` and `yarn-site.xml` on both nodes must have identical configurations
- Delete the output directory before re-running: `hdfs dfs -rm -r /searchengine1/output`
