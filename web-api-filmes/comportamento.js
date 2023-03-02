baseURL= 'http://127.0.0.1:8000/filmes'

let filmes=[]

function atualizar_tela(){
    //manipulacao de DOM
    const ul_filmes = document.getElementById('list-filmes')

    for(let filme of filmes){
        const item = document.createElement('li')
        //const label = '#' + filme.id + '-' + filme.nome + '-' + filme.genero 
        const label = `#${filme.id} - ${filme.nome} - ${filme.genero} `

        const btn_editar = document.createElement('a') //cria tag <a></a> no arquivo.html
        btn_editar.innerText = 'Editar' // cria um test dentro da tag a <a>Editar</a>
        btn_editar.href = '#' //caminho do link da tag a
        btn_editar.onclick = () => {alert('Editar')} //dentro das chaves pode colocar o que precisa fazer quando dar um click

        const btn_remover = document.createElement('a') //cria tag <a></a> no arquivo.html
        btn_remover.innerText = 'Remover' // cria um test dentro da tag a <a>Remover</a>
        btn_remover.href = '#' //caminho do link da tag a
        const espaco = document.createElement('span')
        espaco.innerText = ' '
        btn_remover.onclick = async () => {
            //alert(`Remover o Filme ${filme.nome}!!`)
            //chama a API metodo DELETE passando o ID URL
            const response = await fetch(baseURL+'/'+filme.id, {method:'DELETE'})
            
            // se deu certo..
            if(response.ok){
                alert('Filme removido com sucesso!')
                carregar_filmes()
            }
        }
        

        item.innerText = label
        item.appendChild(btn_editar)
        item.appendChild(espaco)
        item.appendChild(btn_remover)

        ul_filmes.appendChild(item)
    }
}

async function carregar_filmes(){
    console.log('API - Todos os filmes')
    const response = await fetch(baseURL)

    const status = response.status
    filmes = await response.json()

    atualizar_tela()
    //console.log('Status', status)
    //console.log('Dados', dados)
}

function configurar_formulario(){
    const form_filme = document.getElementById('form-filme')
    const input_duracao = document.getElementById('duracao')
    
    form_filme.onsubmit = async function(){
        const dados = form_filme.children
        const nome = dados[0].value
        const genero = dados[1].value
        const ano = Number(dados[2].value)
        const duracao = Number(input_duracao.value)

        const filme = {nome, genero, ano, duracao}

        console.log('submenteu!')
        
        const response = await fetch(baseURL, {
                                                method:'POST',
                                                body: JSON.stringify(filme),
                                                headers: {
                                                    'Content-Type': 'application/json'
                                                }
                                            }
                                    )
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
