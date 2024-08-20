import subprocess
import re

# Configuration
scripts = ['snake-game-mutex.py', 'snake-game-semaforo.py', 'snake-game-exclusao-mutua.py']
runs_per_script = 10

# Regex patterns to capture relevant data
threads_pattern = re.compile(r'Quantidade de threads tentando escrever na zona crítica do mapa: (\d+)')
winner_pattern = re.compile(r'Cobra vencedora:\s+(\d+)')
time_pattern = re.compile(r'Tempo de execução:\s+([\d\.]+)\s+segundos')

# Storage for results
results = {script: {'over_2_threads': 0, 'winner_snakes': {}, 'execution_times': []} for script in scripts}

# Run each script multiple times
for script in scripts:
    print(f"Running {script} {runs_per_script} times...")
    for _ in range(runs_per_script):
        # Run the script and capture output
        result = subprocess.run(['python3', script], capture_output=True, text=True, errors='ignore')
        output = result.stdout
        
        # Count instances where more than 2 threads were in the critical zone
        threads_in_critical_zone = [int(match) for match in threads_pattern.findall(output)]
        if any(t > 1 for t in threads_in_critical_zone):
            results[script]['over_2_threads'] += 1
        
        # Capture the winning snake
        winner_match = winner_pattern.search(output)
        if winner_match:
            winner_snake = winner_match.group(1)
            if winner_snake in results[script]['winner_snakes']:
                results[script]['winner_snakes'][winner_snake] += 1
            else:
                results[script]['winner_snakes'][winner_snake] = 1
        
        # Capture the execution time
        time_match = time_pattern.search(output)
        if time_match:
            execution_time = float(time_match.group(1))
            results[script]['execution_times'].append(execution_time)

# Generate the report
report = []
for script, data in results.items():
    report.append(f"Report for {script}:")
    report.append(f"  - Number of times more than 1 thread were in the critical zone: {data['over_2_threads']}")
    
    # Summary of winning snakes
    report.append("  - Winning snakes:")
    for snake, count in data['winner_snakes'].items():
        report.append(f"      Snake {snake}: {count} wins")
    
    # Summary of execution times
    if data['execution_times']:
        avg_time = sum(data['execution_times']) / len(data['execution_times'])
        report.append(f"  - Average execution time: {avg_time:.2f} seconds")
    else:
        report.append("  - No execution times recorded")
    
    report.append("")

# Print the report
report_content = "\n".join(report)
print(report_content)

# Optionally, save the report to a file
with open("snake_game_report.txt", "w") as report_file:
    report_file.write(report_content)
