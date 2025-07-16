# Sugestões de Melhorias para o Código SPC Charts

Este documento contém sugestões para melhorar o código `spc_charts.py`, visando maior robustez, flexibilidade e usabilidade.

## 1. Documentação e Docstrings

### Situação Atual

O código não possui documentação adequada nas funções e classes.

### Implementação Recomendada

```python
class SPCCharts:
    """
    Implementa gráficos de Controle Estatístico de Processos (CEP).
    
    Esta classe fornece métodos para criar diferentes tipos de gráficos de controle
    estatístico, incluindo gráficos X-barra e R, I-MR, P, e análise de capacidade.
    
    Parâmetros
    ----------
    data : pandas.DataFrame, pandas.Series, array-like
        Dados para análise de controle estatístico.
        
    Exemplos
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> data = pd.DataFrame(np.random.normal(10, 1, (20, 5)))
    >>> spc = SPCCharts(data)
    >>> fig = spc.x_r_chart()
    """
    
    def x_r_chart(self, subgroup_size=5):
        """
        Cria gráficos X-barra e R para dados em subgrupos.
        
        Parâmetros
        ----------
        subgroup_size : int, opcional
            Tamanho do subgrupo (default=5). Deve estar entre 2 e 10.
        
        Retorna
        -------
        matplotlib.figure.Figure
            Figura contendo os gráficos X-barra e R
            
        Raises
        ------
        ValueError
            Se o tamanho do subgrupo não for suportado
        """
```

## 2. Tabela de Constantes para Diferentes Tamanhos de Subgrupo

### Problema Atual
O código usa constantes fixas para subgrupos de tamanho 5, gerando apenas um aviso para outros tamanhos.

### Solução Proposta
```python
def x_r_chart(self, subgroup_size=5):
    # Tabela de constantes para diferentes tamanhos de subgrupo (n=2 a n=10)
    constants = {
        2: {'A2': 1.880, 'D3': 0, 'D4': 3.267},
        3: {'A2': 1.023, 'D3': 0, 'D4': 2.575},
        4: {'A2': 0.729, 'D3': 0, 'D4': 2.282},
        5: {'A2': 0.577, 'D3': 0, 'D4': 2.114},
        6: {'A2': 0.483, 'D3': 0, 'D4': 2.004},
        7: {'A2': 0.419, 'D3': 0.076, 'D4': 1.924},
        8: {'A2': 0.373, 'D3': 0.136, 'D4': 1.864},
        9: {'A2': 0.337, 'D3': 0.184, 'D4': 1.816},
        10: {'A2': 0.308, 'D3': 0.223, 'D4': 1.777}
    }
    
    if subgroup_size not in constants:
        raise ValueError(f"Tamanho de subgrupo {subgroup_size} não suportado. "
                        f"Valores suportados: {list(constants.keys())}")
    
    A2 = constants[subgroup_size]['A2']
    D3 = constants[subgroup_size]['D3']
    D4 = constants[subgroup_size]['D4']
    
    # Verificar se os dados têm o número correto de colunas
    if self.data.shape[1] != subgroup_size:
        print(f"Aviso: Os dados têm {self.data.shape[1]} colunas, "
              f"mas subgroup_size é {subgroup_size}")
```

## 3. Validação de Dados de Entrada

### Problema Atual
Não há validação adequada dos dados de entrada.

### Solução Proposta
```python
def __init__(self, data):
    """
    Inicializa o objeto SPCCharts com validação de dados.
    """
    if data is None:
        raise ValueError("Os dados não podem ser None")
    
    # Converter para pandas se necessário
    if not isinstance(data, (pd.DataFrame, pd.Series)):
        try:
            data = pd.DataFrame(data) if hasattr(data, '__len__') and len(data) > 0 else pd.Series(data)
        except Exception as e:
            raise ValueError(f"Não foi possível converter os dados: {e}")
    
    if len(data) == 0:
        raise ValueError("Os dados não podem estar vazios")
    
    # Verificar se há valores NaN
    if data.isnull().any().any() if isinstance(data, pd.DataFrame) else data.isnull().any():
        print("Aviso: Os dados contêm valores NaN que podem afetar os cálculos")
    
    self.data = data
    self._setup_style()

def _setup_style(self):
    """Configura o estilo padrão para os gráficos."""
    self.style = {
        'figsize': (12, 8),
        'grid': True,
        'central_line_color': 'green',
        'limit_line_color': 'red',
        'data_fmt': 'bo-',
        'range_fmt': 'ro-',
        'alpha': 0.7
    }
```

## 4. Método para Normalização de Dados

### Solução Proposta
```python
def _normalize_data(self, data=None):
    """
    Normaliza diferentes formatos de dados para um formato padrão.
    
    Parâmetros
    ----------
    data : pandas.DataFrame, pandas.Series, array-like, opcional
        Dados para normalizar. Se None, usa self.data.
        
    Retorna
    -------
    pandas.Series ou pandas.DataFrame
        Dados normalizados
        
    Raises
    ------
    ValueError
        Se o formato de dados não for suportado
    """
    data = self.data if data is None else data
    
    if isinstance(data, pd.DataFrame):
        return data
    elif isinstance(data, pd.Series):
        return data
    elif isinstance(data, (list, tuple, np.ndarray)):
        try:
            return pd.Series(data)
        except Exception as e:
            raise ValueError(f"Não foi possível converter os dados: {e}")
    else:
        raise ValueError(f"Formato de dados não suportado: {type(data)}")
```

## 5. Funcionalidade de Exportação

### Solução Proposta
```python
def export_data(self, filename, format='csv', include_calculations=False):
    """
    Exporta os dados e opcionalmente os cálculos para um arquivo.
    
    Parâmetros
    ----------
    filename : str
        Nome base do arquivo (sem extensão)
    format : str, opcional
        Formato de exportação ('csv', 'excel', 'json')
    include_calculations : bool, opcional
        Se True, inclui cálculos como médias e limites de controle
        
    Raises
    ------
    ValueError
        Se o formato não for suportado
    """
    if not isinstance(self.data, (pd.DataFrame, pd.Series)):
        raise TypeError("Dados devem ser DataFrame ou Series para exportação")
    
    # Preparar dados para exportação
    export_data = self.data.copy()
    
    if include_calculations and isinstance(self.data, pd.DataFrame):
        # Adicionar cálculos como novas colunas
        export_data['X_bar'] = self.data.mean(axis=1)
        export_data['R'] = self.data.max(axis=1) - self.data.min(axis=1)
    
    # Exportar conforme o formato
    if format.lower() == 'csv':
        export_data.to_csv(f"{filename}.csv", index=True)
    elif format.lower() == 'excel':
        export_data.to_excel(f"{filename}.xlsx", index=True)
    elif format.lower() == 'json':
        export_data.to_json(f"{filename}.json", orient='index')
    else:
        raise ValueError(f"Formato '{format}' não suportado. "
                        "Formatos disponíveis: 'csv', 'excel', 'json'")
    
    print(f"Dados exportados para {filename}.{format.lower()}")

def save_chart(self, fig, filename, format='png', dpi=300):
    """
    Salva um gráfico em arquivo.
    
    Parâmetros
    ----------
    fig : matplotlib.figure.Figure
        Figura a ser salva
    filename : str
        Nome do arquivo (sem extensão)
    format : str, opcional
        Formato da imagem ('png', 'pdf', 'svg')
    dpi : int, opcional
        Resolução da imagem
    """
    fig.savefig(f"{filename}.{format}", dpi=dpi, bbox_inches='tight')
    print(f"Gráfico salvo como {filename}.{format}")
```

## 6. Melhorias na Análise de Capacidade

### Solução Proposta
```python
def process_capability(self, usl, lsl, target=None):
    """
    Realiza análise de capacidade do processo com interpretação dos resultados.
    
    Parâmetros
    ----------
    usl : float
        Limite Superior de Especificação
    lsl : float
        Limite Inferior de Especificação
    target : float, opcional
        Valor alvo (se não fornecido, usa a média dos limites)
        
    Retorna
    -------
    tuple
        (figura, dicionário com índices e interpretação)
    """
    # ...código de cálculo existente...
    
    # Adicionar valor alvo
    if target is None:
        target = (usl + lsl) / 2
    
    # Calcular índices adicionais
    if std > 0:
        # Cpk tradicional
        cpu = (usl - mean) / (3 * std)
        cpl = (mean - lsl) / (3 * std)
        cpk = min(cpu, cpl)
        
        # Cpm (considerando o valor alvo)
        cpm = (usl - lsl) / (6 * np.sqrt(std**2 + (mean - target)**2))
    else:
        cpu = cpl = cpk = cpm = np.inf
    
    # Interpretação dos resultados
    def interpret_capability(cp_val, cpk_val):
        if cp_val >= 2.0 and cpk_val >= 2.0:
            return "Excelente capacidade"
        elif cp_val >= 1.33 and cpk_val >= 1.33:
            return "Processo capaz"
        elif cp_val >= 1.0 and cpk_val >= 1.0:
            return "Marginalmente capaz"
        else:
            return "Processo não capaz"
    
    interpretation = interpret_capability(cp, cpk)
    
    # Calcular porcentagem de defeitos esperada
    if std > 0:
        z_usl = (usl - mean) / std
        z_lsl = (lsl - mean) / std
        defect_rate = (stats.norm.sf(z_usl) + stats.norm.cdf(z_lsl)) * 100
    else:
        defect_rate = 0
    
    # ...código de plotagem com melhorias...
    
    plt.title(f'Análise de Capacidade do Processo\n'
              f'Cp = {cp:.3f}, Cpk = {cpk:.3f}, Cpm = {cpm:.3f}\n'
              f'{interpretation} - Taxa de defeitos estimada: {defect_rate:.4f}%')
    
    # Adicionar linha do valor alvo
    plt.axvline(target, color='blue', linestyle=':', label=f'Alvo = {target}')
    
    results = {
        'Cp': cp, 'Cpk': cpk, 'Cpm': cpm,
        'CPU': cpu, 'CPL': cpl,
        'Mean': mean, 'Std': std,
        'Target': target,
        'Defect_Rate_Percent': defect_rate,
        'Interpretation': interpretation
    }
    
    return fig, results
```

## 7. Detecção de Padrões Não Aleatórios

### Solução Proposta
```python
def detect_patterns(self, data_series, ucl, lcl, center_line):
    """
    Detecta padrões não aleatórios nos dados (Western Electric Rules).
    
    Parâmetros
    ----------
    data_series : pandas.Series
        Série de dados para análise
    ucl : float
        Limite de controle superior
    lcl : float
        Limite de controle inferior
    center_line : float
        Linha central
        
    Retorna
    -------
    dict
        Dicionário com os padrões detectados
    """
    patterns = {
        'points_beyond_limits': [],
        'seven_consecutive_same_side': [],
        'two_of_three_beyond_2sigma': [],
        'four_of_five_beyond_1sigma': []
    }
    
    # Calcular limites de 1 e 2 sigma
    sigma = (ucl - center_line) / 3
    upper_2sigma = center_line + 2 * sigma
    lower_2sigma = center_line - 2 * sigma
    upper_1sigma = center_line + sigma
    lower_1sigma = center_line - sigma
    
    # Regra 1: Pontos além dos limites de controle
    beyond_limits = (data_series > ucl) | (data_series < lcl)
    patterns['points_beyond_limits'] = data_series.index[beyond_limits].tolist()
    
    # Regra 2: 7 pontos consecutivos do mesmo lado da linha central
    above_center = (data_series > center_line).astype(int)
    below_center = (data_series < center_line).astype(int)
    
    # Implementar detecção de sequências...
    # (código adicional para detectar padrões específicos)
    
    return patterns

def _add_pattern_annotations(self, ax, data_series, patterns):
    """Adiciona anotações visuais para padrões detectados."""
    for idx in patterns['points_beyond_limits']:
        ax.annotate('!', xy=(idx, data_series.iloc[idx]), 
                   xytext=(5, 5), textcoords='offset points',
                   color='red', fontweight='bold', fontsize=12)
```

## 8. Configuração Flexível de Estilos

### Solução Proposta
```python
def update_style(self, **kwargs):
    """
    Atualiza as configurações de estilo dos gráficos.
    
    Parâmetros aceitos: figsize, grid, central_line_color, 
    limit_line_color, data_fmt, range_fmt, alpha
    """
    for key, value in kwargs.items():
        if key in self.style:
            self.style[key] = value
        else:
            print(f"Aviso: Parâmetro de estilo '{key}' não reconhecido")

def apply_theme(self, theme='default'):
    """
    Aplica um tema pré-definido aos gráficos.
    
    Parâmetros
    ----------
    theme : str
        Nome do tema ('default', 'dark', 'colorblind', 'print')
    """
    themes = {
        'default': {
            'central_line_color': 'green',
            'limit_line_color': 'red',
            'data_fmt': 'bo-',
            'range_fmt': 'ro-'
        },
        'dark': {
            'central_line_color': '#00ff00',
            'limit_line_color': '#ff6b6b',
            'data_fmt': 'co-',
            'range_fmt': 'mo-'
        },
        'colorblind': {
            'central_line_color': '#2E8B57',
            'limit_line_color': '#DC143C',
            'data_fmt': 'o-',
            'range_fmt': 's-'
        }
    }
    
    if theme in themes:
        self.style.update(themes[theme])
    else:
        print(f"Tema '{theme}' não encontrado")
```

## Implementação Recomendada

1. **Prioridade Alta**: Documentação (docstrings) e validação de dados
2. **Prioridade Média**: Tabela de constantes e detecção de padrões
3. **Prioridade Baixa**: Funcionalidades de exportação e temas

Essas melhorias tornarão o código mais robusto, fácil de usar e adequado para uso em produção.


# Sugestões de Melhorias para o Código SPC Charts

Este documento contém sugestões para melhorar o código `spc_charts.py`, visando maior robustez, flexibilidade e usabilidade.

## 1. Documentação e Docstrings

### Situação Atual

O código não possui documentação adequada nas funções e classes.

### Implementação Recomendada

```python
class SPCCharts:
    """
    Implementa gráficos de Controle Estatístico de Processos (CEP).
    
    Esta classe fornece métodos para criar diferentes tipos de gráficos de controle
    estatístico, incluindo gráficos X-barra e R, I-MR, P, e análise de capacidade.
    
    Parâmetros
    ----------
    data : pandas.DataFrame, pandas.Series, array-like
        Dados para análise de controle estatístico.
        
    Exemplos
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> data = pd.DataFrame(np.random.normal(10, 1, (20, 5)))
    >>> spc = SPCCharts(data)
    >>> fig = spc.x_r_chart()
    """
    
    def x_r_chart(self, subgroup_size=5):
        """
        Cria gráficos X-barra e R para dados em subgrupos.
        
        Parâmetros
        ----------
        subgroup_size : int, opcional
            Tamanho do subgrupo (default=5). Deve estar entre 2 e 10.
        
        Retorna
        -------
        matplotlib.figure.Figure
            Figura contendo os gráficos X-barra e R
            
        Raises
        ------
        ValueError
            Se o tamanho do subgrupo não for suportado
        """
```

## 2. Tabela de Constantes para Diferentes Tamanhos de Subgrupo

### Problema Atual
O código usa constantes fixas para subgrupos de tamanho 5, gerando apenas um aviso para outros tamanhos.

### Solução Proposta
```python
def x_r_chart(self, subgroup_size=5):
    # Tabela de constantes para diferentes tamanhos de subgrupo (n=2 a n=10)
    constants = {
        2: {'A2': 1.880, 'D3': 0, 'D4': 3.267},
        3: {'A2': 1.023, 'D3': 0, 'D4': 2.575},
        4: {'A2': 0.729, 'D3': 0, 'D4': 2.282},
        5: {'A2': 0.577, 'D3': 0, 'D4': 2.114},
        6: {'A2': 0.483, 'D3': 0, 'D4': 2.004},
        7: {'A2': 0.419, 'D3': 0.076, 'D4': 1.924},
        8: {'A2': 0.373, 'D3': 0.136, 'D4': 1.864},
        9: {'A2': 0.337, 'D3': 0.184, 'D4': 1.816},
        10: {'A2': 0.308, 'D3': 0.223, 'D4': 1.777}
    }
    
    if subgroup_size not in constants:
        raise ValueError(f"Tamanho de subgrupo {subgroup_size} não suportado. "
                        f"Valores suportados: {list(constants.keys())}")
    
    A2 = constants[subgroup_size]['A2']
    D3 = constants[subgroup_size]['D3']
    D4 = constants[subgroup_size]['D4']
    
    # Verificar se os dados têm o número correto de colunas
    if self.data.shape[1] != subgroup_size:
        print(f"Aviso: Os dados têm {self.data.shape[1]} colunas, "
              f"mas subgroup_size é {subgroup_size}")
```

## 3. Validação de Dados de Entrada

### Problema Atual
Não há validação adequada dos dados de entrada.

### Solução Proposta
```python
def __init__(self, data):
    """
    Inicializa o objeto SPCCharts com validação de dados.
    """
    if data is None:
        raise ValueError("Os dados não podem ser None")
    
    # Converter para pandas se necessário
    if not isinstance(data, (pd.DataFrame, pd.Series)):
        try:
            data = pd.DataFrame(data) if hasattr(data, '__len__') and len(data) > 0 else pd.Series(data)
        except Exception as e:
            raise ValueError(f"Não foi possível converter os dados: {e}")
    
    if len(data) == 0:
        raise ValueError("Os dados não podem estar vazios")
    
    # Verificar se há valores NaN
    if data.isnull().any().any() if isinstance(data, pd.DataFrame) else data.isnull().any():
        print("Aviso: Os dados contêm valores NaN que podem afetar os cálculos")
    
    self.data = data
    self._setup_style()

def _setup_style(self):
    """Configura o estilo padrão para os gráficos."""
    self.style = {
        'figsize': (12, 8),
        'grid': True,
        'central_line_color': 'green',
        'limit_line_color': 'red',
        'data_fmt': 'bo-',
        'range_fmt': 'ro-',
        'alpha': 0.7
    }
```

## 4. Método para Normalização de Dados

### Solução Proposta
```python
def _normalize_data(self, data=None):
    """
    Normaliza diferentes formatos de dados para um formato padrão.
    
    Parâmetros
    ----------
    data : pandas.DataFrame, pandas.Series, array-like, opcional
        Dados para normalizar. Se None, usa self.data.
        
    Retorna
    -------
    pandas.Series ou pandas.DataFrame
        Dados normalizados
        
    Raises
    ------
    ValueError
        Se o formato de dados não for suportado
    """
    data = self.data if data is None else data
    
    if isinstance(data, pd.DataFrame):
        return data
    elif isinstance(data, pd.Series):
        return data
    elif isinstance(data, (list, tuple, np.ndarray)):
        try:
            return pd.Series(data)
        except Exception as e:
            raise ValueError(f"Não foi possível converter os dados: {e}")
    else:
        raise ValueError(f"Formato de dados não suportado: {type(data)}")
```

## 5. Funcionalidade de Exportação

### Solução Proposta
```python
def export_data(self, filename, format='csv', include_calculations=False):
    """
    Exporta os dados e opcionalmente os cálculos para um arquivo.
    
    Parâmetros
    ----------
    filename : str
        Nome base do arquivo (sem extensão)
    format : str, opcional
        Formato de exportação ('csv', 'excel', 'json')
    include_calculations : bool, opcional
        Se True, inclui cálculos como médias e limites de controle
        
    Raises
    ------
    ValueError
        Se o formato não for suportado
    """
    if not isinstance(self.data, (pd.DataFrame, pd.Series)):
        raise TypeError("Dados devem ser DataFrame ou Series para exportação")
    
    # Preparar dados para exportação
    export_data = self.data.copy()
    
    if include_calculations and isinstance(self.data, pd.DataFrame):
        # Adicionar cálculos como novas colunas
        export_data['X_bar'] = self.data.mean(axis=1)
        export_data['R'] = self.data.max(axis=1) - self.data.min(axis=1)
    
    # Exportar conforme o formato
    if format.lower() == 'csv':
        export_data.to_csv(f"{filename}.csv", index=True)
    elif format.lower() == 'excel':
        export_data.to_excel(f"{filename}.xlsx", index=True)
    elif format.lower() == 'json':
        export_data.to_json(f"{filename}.json", orient='index')
    else:
        raise ValueError(f"Formato '{format}' não suportado. "
                        "Formatos disponíveis: 'csv', 'excel', 'json'")
    
    print(f"Dados exportados para {filename}.{format.lower()}")

def save_chart(self, fig, filename, format='png', dpi=300):
    """
    Salva um gráfico em arquivo.
    
    Parâmetros
    ----------
    fig : matplotlib.figure.Figure
        Figura a ser salva
    filename : str
        Nome do arquivo (sem extensão)
    format : str, opcional
        Formato da imagem ('png', 'pdf', 'svg')
    dpi : int, opcional
        Resolução da imagem
    """
    fig.savefig(f"{filename}.{format}", dpi=dpi, bbox_inches='tight')
    print(f"Gráfico salvo como {filename}.{format}")
```

## 6. Melhorias na Análise de Capacidade

### Solução Proposta
```python
def process_capability(self, usl, lsl, target=None):
    """
    Realiza análise de capacidade do processo com interpretação dos resultados.
    
    Parâmetros
    ----------
    usl : float
        Limite Superior de Especificação
    lsl : float
        Limite Inferior de Especificação
    target : float, opcional
        Valor alvo (se não fornecido, usa a média dos limites)
        
    Retorna
    -------
    tuple
        (figura, dicionário com índices e interpretação)
    """
    # ...código de cálculo existente...
    
    # Adicionar valor alvo
    if target is None:
        target = (usl + lsl) / 2
    
    # Calcular índices adicionais
    if std > 0:
        # Cpk tradicional
        cpu = (usl - mean) / (3 * std)
        cpl = (mean - lsl) / (3 * std)
        cpk = min(cpu, cpl)
        
        # Cpm (considerando o valor alvo)
        cpm = (usl - lsl) / (6 * np.sqrt(std**2 + (mean - target)**2))
    else:
        cpu = cpl = cpk = cpm = np.inf
    
    # Interpretação dos resultados
    def interpret_capability(cp_val, cpk_val):
        if cp_val >= 2.0 and cpk_val >= 2.0:
            return "Excelente capacidade"
        elif cp_val >= 1.33 and cpk_val >= 1.33:
            return "Processo capaz"
        elif cp_val >= 1.0 and cpk_val >= 1.0:
            return "Marginalmente capaz"
        else:
            return "Processo não capaz"
    
    interpretation = interpret_capability(cp, cpk)
    
    # Calcular porcentagem de defeitos esperada
    if std > 0:
        z_usl = (usl - mean) / std
        z_lsl = (lsl - mean) / std
        defect_rate = (stats.norm.sf(z_usl) + stats.norm.cdf(z_lsl)) * 100
    else:
        defect_rate = 0
    
    # ...código de plotagem com melhorias...
    
    plt.title(f'Análise de Capacidade do Processo\n'
              f'Cp = {cp:.3f}, Cpk = {cpk:.3f}, Cpm = {cpm:.3f}\n'
              f'{interpretation} - Taxa de defeitos estimada: {defect_rate:.4f}%')
    
    # Adicionar linha do valor alvo
    plt.axvline(target, color='blue', linestyle=':', label=f'Alvo = {target}')
    
    results = {
        'Cp': cp, 'Cpk': cpk, 'Cpm': cpm,
        'CPU': cpu, 'CPL': cpl,
        'Mean': mean, 'Std': std,
        'Target': target,
        'Defect_Rate_Percent': defect_rate,
        'Interpretation': interpretation
    }
    
    return fig, results
```

## 7. Detecção de Padrões Não Aleatórios

### Solução Proposta
```python
def detect_patterns(self, data_series, ucl, lcl, center_line):
    """
    Detecta padrões não aleatórios nos dados (Western Electric Rules).
    
    Parâmetros
    ----------
    data_series : pandas.Series
        Série de dados para análise
    ucl : float
        Limite de controle superior
    lcl : float
        Limite de controle inferior
    center_line : float
        Linha central
        
    Retorna
    -------
    dict
        Dicionário com os padrões detectados
    """
    patterns = {
        'points_beyond_limits': [],
        'seven_consecutive_same_side': [],
        'two_of_three_beyond_2sigma': [],
        'four_of_five_beyond_1sigma': []
    }
    
    # Calcular limites de 1 e 2 sigma
    sigma = (ucl - center_line) / 3
    upper_2sigma = center_line + 2 * sigma
    lower_2sigma = center_line - 2 * sigma
    upper_1sigma = center_line + sigma
    lower_1sigma = center_line - sigma
    
    # Regra 1: Pontos além dos limites de controle
    beyond_limits = (data_series > ucl) | (data_series < lcl)
    patterns['points_beyond_limits'] = data_series.index[beyond_limits].tolist()
    
    # Regra 2: 7 pontos consecutivos do mesmo lado da linha central
    above_center = (data_series > center_line).astype(int)
    below_center = (data_series < center_line).astype(int)
    
    # Implementar detecção de sequências...
    # (código adicional para detectar padrões específicos)
    
    return patterns

def _add_pattern_annotations(self, ax, data_series, patterns):
    """Adiciona anotações visuais para padrões detectados."""
    for idx in patterns['points_beyond_limits']:
        ax.annotate('!', xy=(idx, data_series.iloc[idx]), 
                   xytext=(5, 5), textcoords='offset points',
                   color='red', fontweight='bold', fontsize=12)
```

## 8. Configuração Flexível de Estilos

### Solução Proposta
```python
def update_style(self, **kwargs):
    """
    Atualiza as configurações de estilo dos gráficos.
    
    Parâmetros aceitos: figsize, grid, central_line_color, 
    limit_line_color, data_fmt, range_fmt, alpha
    """
    for key, value in kwargs.items():
        if key in self.style:
            self.style[key] = value
        else:
            print(f"Aviso: Parâmetro de estilo '{key}' não reconhecido")

def apply_theme(self, theme='default'):
    """
    Aplica um tema pré-definido aos gráficos.
    
    Parâmetros
    ----------
    theme : str
        Nome do tema ('default', 'dark', 'colorblind', 'print')
    """
    themes = {
        'default': {
            'central_line_color': 'green',
            'limit_line_color': 'red',
            'data_fmt': 'bo-',
            'range_fmt': 'ro-'
        },
        'dark': {
            'central_line_color': '#00ff00',
            'limit_line_color': '#ff6b6b',
            'data_fmt': 'co-',
            'range_fmt': 'mo-'
        },
        'colorblind': {
            'central_line_color': '#2E8B57',
            'limit_line_color': '#DC143C',
            'data_fmt': 'o-',
            'range_fmt': 's-'
        }
    }
    
    if theme in themes:
        self.style.update(themes[theme])
    else:
        print(f"Tema '{theme}' não encontrado")
```

## Implementação Recomendada

1. **Prioridade Alta**: Documentação (docstrings) e validação de dados
2. **Prioridade Média**: Tabela de constantes e detecção de padrões
3. **Prioridade Baixa**: Funcionalidades de exportação e temas

Essas melhorias tornarão o código mais robusto, fácil de usar e adequado para uso em produção.
