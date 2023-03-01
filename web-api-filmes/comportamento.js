baseURL= 'http://127.0.0.1:8000/filmes'

let filmes=[]

functionatualizar_tela(){
    //manipulacao de DOM
    const ul_filmes = document.getElementById('list-fime')

    for(let filme of filmes){
        const item = document.createElement('li')
        item.innerText = filme.nome

        ul_filmes.appendChild(item)
    }
}

async function carregar_filmes(){
    console.log('API - Todos os filmes')
    const response = await fetch(baseURL)

    const status = response.status
    filmes = await response.json()

    atualizar_tela()
}

function configurar_formulario(){
    const form_filme = document.getElementById('form-filme')
    const input_duracao = document.getElementById('duracao')
    
    form_filme.onsubmit = async function(){
        const dados = form_filme.children
        const nome = dados[0].value
        const genero = dados[1].value
        const ano = dados[2].value
        const duracao = input_duracao.value

        const filme = {nome, genero, ano, duracao}

        console.log('submenteu!')
        
        const response = await fetch(baseURL, {
            method:'POST',
            body: JSON.stringify(filme),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        if(response.status === 201){
            alert('Filme Adicionadado com sucesso!')
        }else{
            alert('Não foi possivel adicionar.')
        }
    }    
}

function app(){
    console.log('Hello Filmes')
    configurar_formulario()
    carregar_filmes()
}

app()
