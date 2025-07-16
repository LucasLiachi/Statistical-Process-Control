import pandas as pd
import numpy as np

def generate_manufacturing_data(n_subgroups=25, subgroup_size=5, process_mean=10.0, process_std=0.5):
    """Gera dados simulados de processo de manufatura para gráficos X-R"""
    np.random.seed(42)
    
    samples = []
    for i in range(n_subgroups):
        subgroup = np.random.normal(process_mean, process_std, subgroup_size)
        samples.append(subgroup)
    
    return pd.DataFrame(samples, columns=[f'Measurement_{i+1}' for i in range(subgroup_size)])

def generate_defects_data(n_samples=30, avg_inspected=100, avg_defects=5):
    """Gera dados de defeitos para gráficos de atributos"""
    np.random.seed(42)
    
    data = {
        'sample': range(1, n_samples + 1),
        'inspected': np.random.randint(avg_inspected - 20, avg_inspected + 20, n_samples),
        'defective': np.random.poisson(avg_defects, n_samples)
    }
    
    return pd.DataFrame(data)

def generate_individual_measurements(n_points=50, target=20.0, sigma=1.0):
    """Gera dados de medições individuais para gráfico I-MR"""
    np.random.seed(42)
    
    # Simular algumas causas especiais
    data = np.random.normal(target, sigma, n_points)
    
    # Introduzir alguns pontos fora de controle
    data[15:18] += 2.5  # Shift no processo
    data[35] += 4.0     # Ponto isolado
    
    return pd.Series(data, name='measurements')

def generate_process_capability_data(n_samples=1000, target=50.0, sigma=2.0):
    """Gera dados para análise de capacidade do processo"""
    np.random.seed(42)
    
    data = np.random.normal(target, sigma, n_samples)
    
    return pd.Series(data, name='process_data')

if __name__ == "__main__":
    # Gerar e salvar datasets exemplo
    
    # Dados para gráfico X-R
    xr_data = generate_manufacturing_data()
    xr_data.to_csv('xr_chart_data.csv', index=False)
    
    # Dados para gráfico p
    p_data = generate_defects_data()
    p_data.to_csv('p_chart_data.csv', index=False)
    
    # Dados para gráfico I-MR
    imr_data = generate_individual_measurements()
    imr_data.to_csv('imr_chart_data.csv', index=False)
    
    # Dados para capacidade
    capability_data = generate_process_capability_data()
    capability_data.to_csv('capability_data.csv', index=False)
    
    print("✅ Datasets gerados com sucesso!")
