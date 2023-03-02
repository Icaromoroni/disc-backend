baseURL= 'http://127.0.0.1:8000/filmes'

let filmes=[]

function atualizar_tela(){
    //manipulacao de DOM
    const ul_filmes = document.getElementById('list-filme')

    for(let filme of filmes){
        const item = document.createElement('li')
        const label = `#${filme.id} - ${filme.nome} - ${filme.genero}`

        const bnt_editar = document.createElement('a')
        bnt_editar.innerText = 'Editar'
        bnt_editar.href = '#'
        bnt_editar.onclick = () => {alert('Editar')}
        const bnt_remover = document.createElement('span')
        bnt_remover.innerText = 'Remover'
        bnt_remover.href = '#'
        bnt_remover.onclick = () => {alert('Remover')}

        item.innerText = label
        item.appendChild(bnt_editar)
        item.appendChild(bnt_remover)

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
