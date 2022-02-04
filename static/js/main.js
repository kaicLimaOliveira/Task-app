var dados = {
    "clientes": [
        {
            "id": "1",
            "nome": "João Luiz",
            "cpf": "567.234.789-43",
            "valor_debito": 1000.00,
            "dias_atraso": 678,
            "produto": "Cartão Renner SS",
            "desconto": 50
        },
        {
            "id": "2",
            "nome": "Vitor Zambon",
            "cpf": "645.234.009-41",
            "valor_debito": 5000.00,
            "dias_atraso": 878,
            "produto": "Cartão Americanas SS",
            "desconto": 60
        }, {
            "id": "3",
            "nome": "Arthur Trevisan",
            "cpf": "889.034.900-22",
            "valor_debito": 4000.00,
            "dias_atraso": 128,
            "produto": "Cartão Itaú SS",
            "desconto": 30
        }, {
            "id": "4",
            "nome": "Ravi Sachs",
            "cpf": "875.223.777-13",
            "valor_debito": 3000.00,
            "dias_atraso": 508,
            "produto": "Cartão Bradesco SS",
            "desconto": 80
        }, {
            "id": "5",
            "nome": "Gustavo Giraldi Silva",
            "cpf": "677.345.119-01",
            "valor_debito": 2000.00,
            "dias_atraso": 1089,
            "produto": "Cartão Santander SS",
            "desconto": 70
        }
    ]

}

$(document).ready(() => {

    $('#btn-submit').on('click', e => {
        $('#aside-text').empty()
        let template = $('#text').val()

        e.preventDefault()

        if (template == '' || $('#fileName').val() == '') {
            sweetAlert('error', 'Oops...', 'Seu texto está vazio e precisa ser preenchido')
        } else {
            $('#formImport').submit()
            dados.clientes.forEach((users) => {
                let textOriginal = template
                let textLower = template.toLowerCase()

                Object.entries(users).forEach(([key, value]) => {
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

                $('#aside-text').append(`${textOriginal}<br /> <hr />`)
            })
        }
    })

    $('#btn-reset').click(() => {
        $('#text').val()
        $('#aside-text').empty()
    })


    $('#create-variable').click(() => {
        const name_variable = $('#new-name-variable').val().toLowerCase()
        const value_variable = $('#new-value-variable').val().toLowerCase()

        if (!name_variable && !value_variable) {
            sweetAlert('warning', 'Oops...', 'Sua variável ou seu valor está vazio')
        }
        else {
            if (!value_variable) {
                dados.clientes.forEach((users) => {

                    users[name_variable] = 'valor indefinido'
                    sweetAlert('success', '', '')

                })
                // $('.variable').append(`<a class="copy-link">#${name_variable}</a>`).addClass('copy-link')
            }
            else {
                let userSelect = $('#selectUsers').val()
                let valueSelect = Object(dados.clientes[userSelect])

                if (userSelect == 'none') {
                    dados.clientes.forEach((users) => {

                        users[name_variable] = value_variable
                        sweetAlert('success', '', '')

                    })
                }

                valueSelect[name_variable] = value_variable
                sweetAlert('success', '', '')
            }
        }
    })

    $('.copy-link').on('click', e => {
        let copy = $(e.target).html()

        navigator.clipboard.writeText(copy)
            .then(res => {
                res = `Texto ${copy} copiado para a transferência`
                $('#aviso').fadeIn(1500)
                $('#aviso').fadeOut(1500)
                $('#aviso').addClass('aviso')
                $('#aviso').empty()
                $('#aviso').append(res)
            })
    })

    function sweetAlert(icon, title, text) {
        Swal.fire({
            icon: icon,
            title: title,
            text: text
        })
    }

})

// var original_text = terms_txt
// var modified_text = terms_txt.toLowerCase()

// for (var variable in terms_variables[contract_id]) {
//     while (modified_text.includes("#" + variable.toString())) {
//         var idx = modified_text.indexOf("#" + variable.toString())
//         var fragment = original_text.slice(idx, idx + (variable.toString().length + 1))
//         original_text = original_text.replace(fragment, terms_variables[contract_id][variable])
//         modified_text = modified_text.replace("#" + variable.toString(), terms_variables[contract_id][variable])
//     }

// }