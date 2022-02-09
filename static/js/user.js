$(document).ready(() => {
    
    const dataClients = async () => {
        
        const codeUser = $('#codeUser').val()
        console.log(codeUser);
        const response = await fetch(`code/${codeUser}`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        })
        .catch(e => console.log(e))
        
        const res = await response.json()
        console.log(res)

        res.forEach((users) => {
            // let textOriginal = template
            // let textLower = template.toLowerCase()

            let textOriginal = `
            Olá #full_name seja bem vindo! <br />
            Sua chave de acesso #access_key <br />
            Acesse seu contrato #contract! <br />
            O valor de entrada foi de #entry_value <br />
            em apenas #parcels_quantity parcelas de <br />
            #parcels_value reais por mês <br />
            Data de expiração: #expire_date <br />
            `
            let textTest = `
            Olá #fuLL_name seja bem vindo! <br />
            Sua chave de acesso #ACCESS_KEY <br />
            Acesse seu contrato #contract! <br />
            O valor de entrada foi de #eNTry_value <br />
            em apenas #parcels_quantity parcelas de <br />
            #parcels_value reais por mês <br />
            Data de expiração: #expiRE_date <br />
            `
            let textLower = textOriginal.toLowerCase()

            Object.entries(users).forEach(([key, value]) => {
                console.log(key);

                const hash = '#' + key
                const nome = new RegExp(hash, 'g')
                const count = (textLower.match(nome) || []).length;
        
                for (let i = 0; i < count; i++) {
                    if (count > 0) {
                        let index = textLower.indexOf(hash)
                        let fragment = textOriginal.slice(index, index + hash.length)
        
                        textOriginal = textOriginal.replace(fragment, value)
                        textLower = textLower.replace(hash, value)
                    }
                }
            })
        
            $('#text-user').append(`${textOriginal}<br /> <hr />`)
        })
    } 
    
    $('#button').on('click', async() => {
        const responseRequest = await dataClients()
        console.log(responseRequest);
    })

    $('#btn-reset').click(() => {
        $('#text-user').empty()
    })
})
