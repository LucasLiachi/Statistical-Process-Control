# ============================================================================
# CONTROLE ESTATÍSTICO DE PROCESSO (CEP) - GRÁFICOS DE CONTROLE
# ============================================================================
# Este módulo implementa os principais gráficos de controle para CEP:
# - Gráficos X-barra e R (para dados por subgrupos)
# - Gráficos I e MR (para dados individuais)
# - Gráfico p (para proporção de defeituosos)
# - Análise de Capacidade do Processo
# ============================================================================

# ============================================================================
# SEÇÃO 1: IMPORTAÇÕES E DEFINIÇÃO DA CLASSE SPCCharts
# ============================================================================
# Esta seção contém todas as importações necessárias para análise estatística
# e visualização, além da definição completa da classe SPCCharts com todos
# os seus métodos. A classe é estruturada para receber dados em diferentes
# formatos (DataFrame, Series ou arrays) e implementa os principais tipos
# de gráficos de controle estatístico de processo:
#
# - Método auxiliar _plot_control_chart: padroniza a plotagem com linha central,
#   UCL/LCL, títulos e formatação visual consistente
# - x_r_chart: para dados coletados em subgrupos, monitora média (X-barra) e
#   variabilidade (R - amplitude) usando constantes A2, D3, D4
# - i_mr_chart: para dados individuais, monitora valores (I) e variabilidade
#   através de amplitudes móveis (MR) usando constantes 2.66 e 3.27
# - p_chart: para dados de atributos, monitora proporção de defeituosos
#   baseado na distribuição binomial
# - process_capability: calcula índices Cp e Cpk comparando variabilidade
#   do processo com limites de especificação, incluindo visualização com
#   histograma e curva normal teórica

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

class SPCCharts:
    """
    Classe para criação e análise de gráficos de Controle Estatístico de Processo
    """
    
    def __init__(self, data):
        """Inicializa a classe com os dados a serem analisados"""
        self.data = data

    def _plot_control_chart(self, ax, series_data, central_line_val, ucl_val, lcl_val,
                              chart_title, series_label, ylabel, xlabel="Sample", 
                              x_values=None, series_fmt='bo-'):
        """
        Método auxiliar para plotar gráficos de controle com formatação padrão
        """
        if x_values is None:
            x_values = range(len(series_data))
        
        ax.plot(x_values, series_data, series_fmt, label=series_label)
        ax.axhline(central_line_val, color='green', linestyle='-', label='Linha Central (Média)')
        ax.axhline(ucl_val, color='red', linestyle='--', label='UCL (Limite Superior)')
        ax.axhline(lcl_val, color='red', linestyle='--', label='LCL (Limite Inferior)')
        ax.set_title(chart_title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.legend()
        ax.grid(True)

    def x_r_chart(self, subgroup_size=5):
        """
        Cria gráficos X-barra e R para controle de processo com dados por subgrupos
        """
        x_bar = self.data.mean(axis=1)
        r_values = self.data.max(axis=1) - self.data.min(axis=1)
        
        x_bar_mean = x_bar.mean()
        r_bar = r_values.mean()
        
        if subgroup_size != 5:
            print(f"Aviso: Constantes A2, D3, D4 são para n=5. Subgroup_size atual é {subgroup_size}.")
        A2, D3, D4 = 0.577, 0, 2.114
        
        ucl_x = x_bar_mean + A2 * r_bar
        lcl_x = x_bar_mean - A2 * r_bar
        ucl_r = D4 * r_bar
        lcl_r = D3 * r_bar
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
        
        self._plot_control_chart(ax1, x_bar, x_bar_mean, ucl_x, lcl_x,
                                 'Gráfico X-barra', 'X-barra', 'Média do Subgrupo')
        
        self._plot_control_chart(ax2, r_values, r_bar, ucl_r, lcl_r,
                                 'Gráfico de Amplitude (R)', 'Amplitude', 'Amplitude do Subgrupo',
                                 series_fmt='ro-')
        
        plt.tight_layout()
        return fig
    
    def i_mr_chart(self):
        """
        Cria gráficos I e MR para controle de processo com dados individuais
        """
        if isinstance(self.data, pd.DataFrame):
            values = self.data.iloc[:, 0].squeeze()
        elif isinstance(self.data, pd.Series):
            values = self.data
        else:
            values = pd.Series(self.data)

        mr_values = np.abs(values.diff().dropna())
        
        values_mean = values.mean()
        mr_bar = mr_values.mean()
        
        ucl_i = values_mean + 2.66 * mr_bar
        lcl_i = values_mean - 2.66 * mr_bar
        
        ucl_mr = 3.27 * mr_bar 
        lcl_mr = 0
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
        
        self._plot_control_chart(ax1, values, values_mean, ucl_i, lcl_i,
                                 'Gráfico de Valores Individuais (I)', 'Valores Individuais', 'Valor Individual')
        
        mr_x_values = values.index[1:] if isinstance(values.index, pd.RangeIndex) else range(1, len(mr_values) + 1)

        self._plot_control_chart(ax2, mr_values, mr_bar, ucl_mr, lcl_mr,
                                 'Gráfico de Amplitude Móvel (MR)', 'Amplitude Móvel', 'Amplitude Móvel',
                                 x_values=mr_x_values, series_fmt='ro-')
        
        plt.tight_layout()
        return fig
    
    def p_chart(self, n_samples):
        """
        Cria gráfico p para controle da proporção de itens defeituosos
        """
        if isinstance(self.data, pd.DataFrame):
            defective_counts = self.data['defective']
        elif isinstance(self.data, pd.Series):
            defective_counts = self.data
        else:
            defective_counts = pd.Series(self.data)

        p_values = defective_counts / n_samples
        p_bar = p_values.mean()
        
        sigma_p = np.sqrt(p_bar * (1 - p_bar) / n_samples)
        ucl_p = p_bar + 3 * sigma_p
        lcl_p = max(0, p_bar - 3 * sigma_p)
        
        fig, ax = plt.subplots(1, 1, figsize=(12, 6))
        
        self._plot_control_chart(ax, p_values, p_bar, ucl_p, lcl_p,
                                 'Gráfico p - Proporção de Defeituosos', 
                                 'Proporção de Defeituosos', 'Proporção', 
                                 xlabel='Amostra')
        
        plt.tight_layout()
        return fig
    
    def process_capability(self, usl, lsl):
        """
        Realiza análise de capacidade do processo calculando índices Cp e Cpk
        """
        if isinstance(self.data, pd.DataFrame):
            data_flat = self.data.values.ravel()
        elif isinstance(self.data, pd.Series):
            data_flat = self.data.values
        else:
            data_flat = np.array(self.data).ravel()
        
        mean = np.mean(data_flat)
        std = np.std(data_flat, ddof=1)
        
        cp = (usl - lsl) / (6 * std) if std > 0 else np.inf
        cpk = np.inf
        if std > 0:
            cpu = (usl - mean) / (3 * std)
            cpl = (mean - lsl) / (3 * std)
            cpk = min(cpu, cpl)
        
        fig = plt.figure(figsize=(10, 6))
        
        plt.hist(data_flat, bins='auto', density=True, alpha=0.7, label='Dados Observados')
        
        if std > 0:
            x_norm = np.linspace(min(data_flat.min(), lsl) - std, max(data_flat.max(), usl) + std, 200)
            plt.plot(x_norm, stats.norm.pdf(x_norm, mean, std), 'r-', label='Distribuição Normal Ajustada')
        
        plt.axvline(usl, color='darkred', linestyle='--', label=f'USL = {usl}')
        plt.axvline(lsl, color='darkred', linestyle='--', label=f'LSL = {lsl}')
        plt.axvline(mean, color='green', linestyle='-', label=f'Média = {mean:.3f}')
        
        plt.title(f'Análise de Capacidade do Processo\nCp = {cp:.3f}, Cpk = {cpk:.3f}')
        plt.xlabel('Valor da Característica')
        plt.ylabel('Densidade de Frequência')
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        return fig, {'Cp': cp, 'Cpk': cpk, 'Mean': mean, 'Std': std}

# ============================================================================
# SEÇÃO 2: GERAÇÃO DE DADOS SIMULADOS PARA DEMONSTRAÇÃO
# ============================================================================
# Esta seção é executada apenas quando o módulo é executado diretamente
# (não importado). Demonstra o uso da classe SPCCharts através de 4 exemplos
# práticos com dados simulados que representam diferentes cenários industriais:
#
# 1. Dados por subgrupos (X-R): simula um processo de produção onde amostras
#    de 5 peças são coletadas periodicamente para monitorar dimensões
# 2. Dados individuais (I-MR): simula um processo químico onde cada medição
#    é custosa e apenas uma observação é feita por vez
# 3. Dados de atributos (p): simula uma linha de inspeção onde itens são
#    classificados como conformes ou não-conformes
# 4. Análise de capacidade: avalia se o processo é capaz de atender
#    especificações definidas pelos limites superior (USL) e inferior (LSL)
#
# Cada exemplo inclui geração de dados realistas, aplicação do método
# apropriado, visualização dos resultados e interpretação estatística

if __name__ == '__main__':
    
    np.random.seed(42)
    
    print("="*60)
    print("EXEMPLO 1: GRÁFICO X-BARRA E R")
    print("="*60)
    print("Gerando dados simulados para 20 subgrupos de tamanho 5...")
    
    data_xr = []
    for _ in range(20):
        subgroup = np.random.normal(loc=10, scale=1, size=5)
        data_xr.append(subgroup)
    
    df_xr = pd.DataFrame(data_xr)
    print(f"Dados gerados: {df_xr.shape[0]} subgrupos de {df_xr.shape[1]} observações cada")

    spc = SPCCharts(df_xr)
    fig_xr = spc.x_r_chart(subgroup_size=5)
    plt.show()

    print("\n" + "="*60)
    print("EXEMPLO 2: GRÁFICO I-MR (VALORES INDIVIDUAIS)")
    print("="*60)
    print("Gerando dados individuais simulados...")
    
    data_imr = pd.Series(np.random.normal(loc=50, scale=2, size=25))
    print(f"Dados gerados: {len(data_imr)} observações individuais")
    
    spc_imr = SPCCharts(data_imr)
    fig_imr = spc_imr.i_mr_chart()
    plt.show()

    print("\n" + "="*60)
    print("EXEMPLO 3: GRÁFICO P (PROPORÇÃO DE DEFEITUOSOS)")
    print("="*60)
    print("Gerando dados de contagem de defeituosos...")
    
    defective_counts = np.random.randint(0, 6, size=30)
    data_p = pd.Series(defective_counts, name='defective')
    n_samples_p = 50
    print(f"Dados gerados: {len(data_p)} amostras de {n_samples_p} itens cada")
    
    spc_p = SPCCharts(data_p)
    fig_p = spc_p.p_chart(n_samples=n_samples_p)
    plt.show()

# ============================================================================
# SEÇÃO 3: ANÁLISE DE CAPACIDADE E INTERPRETAÇÃO DOS RESULTADOS
# ============================================================================
# Esta seção final demonstra a análise de capacidade do processo, que é
# fundamental para determinar se um processo é capaz de produzir dentro das
# especificações estabelecidas. Utiliza os dados do primeiro exemplo para:
#
# - Calcular índices Cp (capacidade potencial): relação entre tolerância
#   especificada e variabilidade natural do processo (6σ)
# - Calcular índice Cpk (capacidade real): considera além da variabilidade,
#   o deslocamento da média do processo em relação ao centro da especificação
# - Gerar visualização comparativa entre distribuição real dos dados e
#   distribuição normal teórica, destacando limites de especificação
# - Interpretar resultados segundo critérios industriais padrão:
#   Cpk ≥ 1.33 (processo capaz), 1.0 ≤ Cpk < 1.33 (marginalmente capaz),
#   Cpk < 1.0 (não capaz)
#
# A análise completa permite tomada de decisão sobre necessidade de ajustes
# no processo, redução de variabilidade ou revisão das especificações

    print("\n" + "="*60)
    print("EXEMPLO 4: ANÁLISE DE CAPACIDADE DO PROCESSO")
    print("="*60)
    print("Realizando análise de capacidade com os dados do Exemplo 1...")
    
    data_cap = df_xr.values.ravel()
    spc_cap = SPCCharts(data_cap)
    
    usl_cap = 13
    lsl_cap = 7
    print(f"Limites de especificação: LSL={lsl_cap}, USL={usl_cap}")
    
    fig_cap, cap_indices = spc_cap.process_capability(usl=usl_cap, lsl=lsl_cap)
    print(f"Índices de Capacidade: {cap_indices}")
    
    print("\nInterpretação dos Índices:")
    print(f"Cp = {cap_indices['Cp']:.3f} - Capacidade potencial")
    print(f"Cpk = {cap_indices['Cpk']:.3f} - Capacidade real")
    if cap_indices['Cpk'] >= 1.33:
        print("Processo CAPAZ (Cpk ≥ 1.33)")
    elif cap_indices['Cpk'] >= 1.0:
        print("Processo MARGINALMENTE CAPAZ (1.0 ≤ Cpk < 1.33)")
    else:
        print("Processo NÃO CAPAZ (Cpk < 1.0)")
    
    plt.show()
    
    print("\n" + "="*60)
    print("ANÁLISE CONCLUÍDA - Todos os gráficos foram gerados!")
    print("="*60)
    # Criação e plotagem do gráfico p
    spc_p = SPCCharts(data_p)
    fig_p = spc_p.p_chart(n_samples=n_samples_p)
    plt.show()

    # ------------------------------------------------------------------------
    # SEÇÃO 3.5: EXEMPLO 4 - ANÁLISE DE CAPACIDADE DO PROCESSO
    # ------------------------------------------------------------------------
    print("\n" + "="*60)
    print("EXEMPLO 4: ANÁLISE DE CAPACIDADE DO PROCESSO")
    print("="*60)
    print("Realizando análise de capacidade com os dados do Exemplo 1...")
    
    # Usando dados do exemplo X-R para análise de capacidade
    data_cap = df_xr.values.ravel()  # Achatando todos os dados
    spc_cap = SPCCharts(data_cap)
    
    # Definindo limites de especificação
    usl_cap = 13  # Limite Superior de Especificação
    lsl_cap = 7   # Limite Inferior de Especificação
    print(f"Limites de especificação: LSL={lsl_cap}, USL={usl_cap}")
    
    # Realização da análise de capacidade
    fig_cap, cap_indices = spc_cap.process_capability(usl=usl_cap, lsl=lsl_cap)
    print(f"Índices de Capacidade: {cap_indices}")
    
    # Interpretação dos resultados
    print("\nInterpretação dos Índices:")
    print(f"Cp = {cap_indices['Cp']:.3f} - Capacidade potencial")
    print(f"Cpk = {cap_indices['Cpk']:.3f} - Capacidade real")
    if cap_indices['Cpk'] >= 1.33:
        print("Processo CAPAZ (Cpk ≥ 1.33)")
    elif cap_indices['Cpk'] >= 1.0:
        print("Processo MARGINALMENTE CAPAZ (1.0 ≤ Cpk < 1.33)")
    else:
        print("Processo NÃO CAPAZ (Cpk < 1.0)")
    
    plt.show()
    
    print("\n" + "="*60)
    print("ANÁLISE CONCLUÍDA - Todos os gráficos foram gerados!")
    print("="*60)
