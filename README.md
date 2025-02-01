# Demonstrações de Rastreamento de Múltiplos e Únicos Objetos no Google Colab

Este repositório contém dois Jupyter Notebooks (`show_multi_tracker.ipynb` e `show_single_tracker.ipynb`) que demonstram o rastreamento de múltiplos e únicos objetos utilizando caixas delimitadoras (bounding boxes) com suporte aprimorado para cores. Esses notebooks são otimizados para uso no **Google Colab**, permitindo que você execute e experimente os códigos diretamente na nuvem, sem a necessidade de configurar um ambiente local.

## Notebooks

### `show_multi_tracker.ipynb`

**Funcionalidade:** Aprimoramento do processamento de frames com suporte a cores para caixas delimitadoras  

Este notebook demonstra o rastreamento de múltiplos objetos em frames de vídeo. A versão aprimorada inclui suporte a cores para as caixas delimitadoras, facilitando a distinção entre os diferentes objetos rastreados. As cores são atribuídas dinamicamente a cada objeto, melhorando a clareza visual e a experiência do usuário.

#### Principais Funcionalidades:
- Rastreamento de múltiplos objetos com caixas delimitadoras.
- Processamento de frames aprimorado com suporte a cores.
- Atribuição dinâmica de cores para melhor distinção dos objetos.
- Pronto para execução no Google Colab.

### `show_single_tracker.ipynb`

**Funcionalidade:** Rastreamento de único objeto com caixas delimitadoras  

Este notebook foca no rastreamento de um único objeto em frames de vídeo. Ele utiliza caixas delimitadoras para destacar o objeto rastreado, com o acréscimo de suporte a cores para a caixa. Essa funcionalidade melhora a visualização do objeto em relação ao fundo.

#### Principais Funcionalidades:
- Rastreamento de único objeto com caixas delimitadoras.
- Suporte a cores para a caixa delimitadora.
- Visualização clara do objeto rastreado.
- Pronto para execução no Google Colab.

---

## Como Usar no Google Colab

Para executar os notebooks no Google Colab, siga os passos abaixo:

1. **Acesse o Google Colab:**
   - Abra o [Google Colab](https://colab.research.google.com/).

2. **Carregue os Notebooks:**
   - Clique em `Arquivo` > `Abrir notebook`.
   - Selecione a aba `GitHub` e cole o link deste repositório.
   - Escolha o notebook que deseja executar (`show_multi_tracker.ipynb` ou `show_single_tracker.ipynb`).

3. **Execute o Código:**
   - Conecte-se a um ambiente de execução clicando em `Conectar` (canto superior direito).
   - Execute as células do notebook sequencialmente para ver os resultados.

---
