# Demonstrações de Rastreamento de Múltiplos e Únicos Objetos no Google Colab

Este repositório contém dois Jupyter Notebooks (`show_multi_tracker.ipynb` e `show_single_tracker.ipynb`) que demonstram o rastreamento de múltiplos e únicos objetos utilizando caixas delimitadoras (bounding boxes). Esses notebooks são otimizados para uso no **Google Colab**, permitindo que você execute e experimente os códigos diretamente na nuvem, sem a necessidade de configurar um ambiente local.

---

## Notebooks

### `show_multi_tracker.ipynb` [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/KauaHenSilva/python_object_tracking_opencv/blob/main/show_multi_tracker.ipynb)

**Funcionalidade:** Rastreamento de múltiplos objetos com suporte a cores dinâmicas para caixas delimitadoras.  

Este notebook demonstra o rastreamento de múltiplos objetos em vídeos utilizando diferentes algoritmos de rastreamento disponíveis no OpenCV. Cada objeto rastreado recebe uma cor única para facilitar a distinção visual. O vídeo processado é exibido diretamente no notebook após a execução.

#### Principais Funcionalidades:
- Rastreamento de múltiplos objetos com caixas delimitadoras.
- Suporte a cores dinâmicas para melhor visualização.
- Algoritmos de rastreamento suportados: BOOSTING, MIL, KCF, MOSSE e CSRT.
- Visualização integrada no Google Colab.

---

### `show_single_tracker.ipynb`  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/KauaHenSilva/python_object_tracking_opencv/blob/main/show_single_tracker.ipynb)

**Funcionalidade:** Rastreamento de único objeto com caixas delimitadoras.  

Este notebook foca no rastreamento de um único objeto em vídeos, utilizando caixas delimitadoras para destacar o objeto rastreado. É ideal para cenários onde o foco é monitorar um único alvo.

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

4. **Teste com Outros Vídeos (Opcional):**
   - Caso queira testar com seus próprios vídeos, use o seguinte código para fazer upload:
     ```python
     from google.colab import files
     uploaded = files.upload()
     ```
   - Substitua o caminho do vídeo no notebook pelo arquivo enviado.

---
