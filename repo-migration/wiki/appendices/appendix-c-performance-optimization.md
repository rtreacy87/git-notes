# Appendix C: Performance Optimization

## Overview

Migrating folders with history can be resource-intensive, especially for large repositories with extensive history. This guide provides techniques and best practices for optimizing performance during migrations, helping you complete the process efficiently even with limited resources.

## Techniques for Handling Large Repositories

### Shallow Cloning

For repositories with extensive history, shallow cloning can significantly reduce the initial download size and processing time.

```bash
# Clone with limited history depth
git clone --depth 100 https://source-repository-url.git source-repo
cd source-repo

# Fetch additional history if needed
git fetch --deepen 100

# Extract the folder with limited history
git filter-repo --path path/to/folder/
```

#### When to Use Shallow Cloning

- When the full history is not required
- For initial testing of the migration process
- When working with limited bandwidth or storage

#### Limitations

- May lose some historical context
- Not suitable when complete history preservation is critical
- Some Git operations may behave differently with shallow clones

### Sparse Checkout

Sparse checkout allows you to check out only specific parts of a repository, reducing the working directory size.

```bash
# Initialize a new repository
mkdir extracted-folder
cd extracted-folder
git init

# Add the source repository as a remote
git remote add origin https://source-repository-url.git

# Configure sparse checkout
git config core.sparseCheckout true
echo "path/to/folder/" > .git/info/sparse-checkout

# Fetch the repository
git fetch origin

# Checkout the main branch
git checkout origin/main

# Now extract the folder with git filter-repo
git filter-repo --path path/to/folder/ --path-rename path/to/folder/:./
```

#### When to Use Sparse Checkout

- When you only need a specific folder from a large repository
- When working with limited disk space
- For repositories with many large binary files

#### Limitations

- More complex setup than standard cloning
- May still download the entire Git history
- Not as efficient as shallow cloning for reducing initial download size

### Incremental Processing

For extremely large repositories, process the history in chunks to reduce memory usage.

```bash
#!/bin/bash
# incremental_migration.sh

SOURCE_REPO=$1
FOLDER_PATH=$2
CHUNK_SIZE=500  # Number of commits per chunk

# Clone source repository
git clone $SOURCE_REPO source-repo
cd source-repo

# Get total number of commits affecting the folder
TOTAL_COMMITS=$(git log --oneline -- $FOLDER_PATH | wc -l)
echo "Total commits affecting $FOLDER_PATH: $TOTAL_COMMITS"

# Calculate number of chunks
CHUNKS=$(( ($TOTAL_COMMITS + $CHUNK_SIZE - 1) / $CHUNK_SIZE ))
echo "Processing in $CHUNKS chunks of $CHUNK_SIZE commits each"

# Create a new repository for the result
mkdir -p ../result-repo
cd ../result-repo
git init

# Process each chunk
for (( i=0; i<$CHUNKS; i++ ))
do
    SKIP=$(( i * $CHUNK_SIZE ))
    TAKE=$CHUNK_SIZE
    
    echo "Processing chunk $((i+1))/$CHUNKS (commits $SKIP to $((SKIP+TAKE)))"
    
    # Create a temporary directory for this chunk
    mkdir -p ../chunk-$i
    cd ../chunk-$i
    
    # Clone source repo for this chunk
    git clone ../source-repo .
    
    # Get the commit range for this chunk
    START_COMMIT=$(git log --skip=$SKIP --max-count=1 --format=%H -- $FOLDER_PATH)
    END_COMMIT=$(git log --skip=$(($SKIP+$TAKE-1)) --max-count=1 --format=%H -- $FOLDER_PATH)
    
    # If we're at the end, use HEAD as the end commit
    if [ -z "$END_COMMIT" ]; then
        END_COMMIT="HEAD"
    fi
    
    echo "Commit range: $START_COMMIT to $END_COMMIT"
    
    # Extract the folder for this commit range
    git filter-repo --path $FOLDER_PATH/ --refs $START_COMMIT..$END_COMMIT
    
    # Go to the result repo
    cd ../result-repo
    
    # Add the chunk repo as a remote
    git remote add chunk-$i ../chunk-$i
    git fetch chunk-$i
    
    # Merge the chunk
    git merge --allow-unrelated-histories chunk-$i/main
    
    # Remove the remote
    git remote remove chunk-$i
    
    # Go back to the main directory
    cd ..
    
    # Clean up the chunk directory
    rm -rf chunk-$i
    
    echo "Completed chunk $((i+1))/$CHUNKS"
done

echo "Migration completed!"
```

#### When to Use Incremental Processing

- For repositories with tens of thousands of commits
- When memory constraints prevent processing the entire history at once
- When you need to monitor progress during a long-running migration

#### Limitations

- More complex implementation
- May take longer overall due to overhead
- Requires careful handling of merge conflicts between chunks

## Hardware Recommendations

### CPU Considerations

Git operations, especially those involving history rewriting, can benefit from multiple CPU cores.

| Repository Size | Recommended CPU |
|-----------------|-----------------|
| Small (<1GB) | 2+ cores |
| Medium (1-5GB) | 4+ cores |
| Large (>5GB) | 8+ cores |

#### Optimizing for CPU

```bash
# Configure Git to use multiple threads for packing
git config --global pack.threads 4  # Adjust based on available cores

# Use parallel compression when possible
git config --global core.compression 9  # Higher values use more CPU but better compression
```

### Memory Requirements

Memory is often the limiting factor for large repository operations.

| Repository Size | Recommended RAM |
|-----------------|-----------------|
| Small (<1GB) | 4GB+ |
| Medium (1-5GB) | 8GB+ |
| Large (>5GB) | 16GB+ |
| Very Large (>10GB) | 32GB+ |

#### Optimizing for Memory

```bash
# Increase Git's memory buffer
git config --global pack.windowMemory "100m"
git config --global pack.packSizeLimit "100m"

# Disable the garbage collector during migration
git config --global gc.auto 0
```

### Disk Space Considerations

Git operations require significant temporary disk space, especially during history rewriting.

| Repository Size | Recommended Free Space |
|-----------------|------------------------|
| Small (<1GB) | 3x repository size |
| Medium (1-5GB) | 4x repository size |
| Large (>5GB) | 5x repository size |

#### Optimizing for Disk Space

```bash
# Clean up unnecessary files before migration
git gc --aggressive --prune=now

# Use a disk with fast I/O (SSD recommended)
# If using an external drive, ensure it has a fast connection (USB 3.0+)

# Monitor disk usage during migration
du -sh .git/objects
```

## Caching and Network Considerations

### Git Credential Caching

Avoid repeated authentication prompts during long-running operations.

```bash
# Cache credentials for 1 hour
git config --global credential.helper 'cache --timeout=3600'

# Store credentials permanently (use with caution)
git config --global credential.helper store
```

### Network Optimization

For repositories hosted on remote servers, network bandwidth can be a bottleneck.

```bash
# Clone without checking out files initially
git clone --no-checkout https://repository-url.git
cd repository
git checkout main

# Compress data during transfer
git config --global core.compression 9

# Use a specific SSH key for faster authentication
git config core.sshCommand "ssh -i ~/.ssh/specific_key -F /dev/null"
```

### Proxy Considerations

When working behind a proxy:

```bash
# Configure Git to use proxy
git config --global http.proxy http://proxy.example.com:8080
git config --global https.proxy http://proxy.example.com:8080

# For specific repositories only
git config http.proxy http://proxy.example.com:8080
git config https.proxy http://proxy.example.com:8080
```

## Optimizing Git Filter-Repo Performance

Git filter-repo is already highly optimized, but these techniques can further improve performance.

### Limiting the Scope

```bash
# Process only specific branches instead of all refs
git filter-repo --path path/to/folder/ --refs refs/heads/main

# Exclude binary files if not needed
git filter-repo --path path/to/folder/ --path-glob '*.bin' --invert-paths --path-glob '*.bin'
```

### Disabling Unnecessary Features

```bash
# Disable blob filtering when only path filtering is needed
git filter-repo --path path/to/folder/ --no-blob-callback

# Skip analyzing the repository
git filter-repo --path path/to/folder/ --no-analyze
```

### Parallel Processing

For multi-folder migrations, process folders in parallel:

```bash
#!/bin/bash
# parallel_extraction.sh

SOURCE_REPO=$1
FOLDERS=("folder1" "folder2" "folder3" "folder4")

# Clone the source repository
git clone $SOURCE_REPO source-repo

# Process each folder in parallel
for folder in "${FOLDERS[@]}"; do
    (
        echo "Processing $folder"
        mkdir -p "extracted-$folder"
        cd "extracted-$folder"
        git clone ../source-repo .
        git filter-repo --path "$folder/" --path-rename "$folder/:/"
        echo "Completed $folder"
    ) &
done

# Wait for all parallel processes to complete
wait

echo "All extractions completed"
```

## Performance Benchmarks

These benchmarks provide a reference for estimating migration times based on repository size and hardware.

| Repository Size | Commits | Files | Hardware | Extraction Time | Import Time |
|-----------------|---------|-------|----------|-----------------|-------------|
| Small (100MB) | 1,000 | 1,000 | 4 cores, 8GB RAM, SSD | ~2 minutes | ~1 minute |
| Medium (1GB) | 5,000 | 10,000 | 4 cores, 16GB RAM, SSD | ~10 minutes | ~5 minutes |
| Large (5GB) | 20,000 | 50,000 | 8 cores, 32GB RAM, SSD | ~45 minutes | ~20 minutes |
| Very Large (10GB+) | 50,000+ | 100,000+ | 16 cores, 64GB RAM, SSD | 2+ hours | 1+ hours |

### Factors Affecting Performance

- **Commit Density**: More commits affecting the target folder increase processing time
- **File Size**: Large binary files slow down processing
- **Branching Complexity**: Complex branch structures take longer to process
- **Disk I/O Speed**: SSD vs. HDD makes a significant difference
- **Network Bandwidth**: Affects initial clone and final push times

## Cloud-based Solutions

For extremely large repositories or limited local resources, consider cloud-based solutions.

### Using Cloud VMs

```bash
# Example: Using a high-memory AWS EC2 instance
# 1. Launch an r5.2xlarge instance (8 vCPUs, 64GB RAM)
# 2. Clone the repository to the instance
# 3. Perform the migration
# 4. Push the results
# 5. Terminate the instance
```

### Containerized Approach

```dockerfile
# Dockerfile for migration container
FROM alpine:latest

RUN apk add --no-cache git python3 py3-pip
RUN pip3 install git-filter-repo

WORKDIR /migration

COPY migrate.sh /migration/
RUN chmod +x /migration/migrate.sh

ENTRYPOINT ["/migration/migrate.sh"]
```

```bash
# Build and run the container
docker build -t git-migration .
docker run -v /path/to/repos:/migration/repos git-migration
```

## Monitoring and Debugging Performance Issues

### Monitoring Git Operations

```bash
# Enable Git trace
export GIT_TRACE=1
export GIT_TRACE_PERFORMANCE=1

# Run the migration command
git filter-repo --path path/to/folder/

# Disable trace when done
unset GIT_TRACE
unset GIT_TRACE_PERFORMANCE
```

### Identifying Bottlenecks

```bash
# Monitor CPU usage
top -b -n 1 | grep git

# Monitor memory usage
ps -o pid,user,%mem,command ax | grep git

# Monitor disk I/O
iostat -x 5

# Monitor network usage
iftop -B
```

### Common Performance Issues and Solutions

| Issue | Symptoms | Solution |
|-------|----------|----------|
| High memory usage | System becomes unresponsive, process killed | Use incremental processing or increase swap space |
| Slow disk I/O | High wait time in top/iostat | Move to SSD, use tmpfs for temporary files |
| Network bottleneck | Slow clone/push operations | Use shallow cloning, work during off-peak hours |
| CPU bottleneck | High CPU usage, low memory/disk activity | Increase pack.threads, use a machine with more cores |

## Next Steps

After optimizing your migration process for performance, refer to the following resources:

- [Advanced Scenarios and Troubleshooting](../wiki-08-advanced-scenarios.md)
- [Best Practices and Case Studies](../wiki-09-best-practices.md)
- [Appendix D: Security Considerations](./appendix-d-security-considerations.md)

## See Also

- [Extracting the Folder with its History](../wiki-04-extracting-folder-history.md)
- [Automation Options](../wiki-06-automation-options.md)
- [Appendix B: Command Reference](./appendix-b-command-reference.md)
