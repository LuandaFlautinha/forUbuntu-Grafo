# Verificar se o ambiente conda já existe
if ! conda env list | grep -q "Grafo_final"
then
    echo "Criando ambiente conda 'Grafo_final'..."
    conda create --name Grafo_final
    conda activate Grafo_final

    # Instalar as bibliotecas necessárias
    echo "Instalando bibliotecas necessárias..."
    conda install -y -c conda-forge networkx pyvis numpy
fi

# Ativar o ambiente conda
echo "Ativando ambiente conda 'Grafo_final'..."
conda activate Grafo_final

# Executar o código Python
echo "Executando grafo_final.py..."
python3 grafo_final.py 



