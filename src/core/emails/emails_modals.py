from src.core.emails.utils import default_document

def test_email(env) -> str:
    main = f''' 
    <table role="presentation" width="100%" style="padding: 20px; padding-top: 50px; text-align: center; margin-top: 50px; border-top: 2px #fff solid;">
        <tr style="background-color: #29434a;">
            <td>
                <h1 style="font-family: 'Courier New', monospace; margin-top: 40px; margin-bottom: 30px;  color: #fff;">Este é um e-mail de teste!</h1>
                <p style="font-family: Arial, sans-serif; color: #fff;">😮‍💨 <strong>Fique tranquilo!</strong> Este email é apenas um teste enviado para que a configuração do seu e-mail foi realizada com sucesso.</p>
                <p style="font-family: Arial, sans-serif; color: #fff;">✅ <strong>Configuração bem-sucedida!</strong> O fato de você ter recebido este e-mail mostra que está tudo funcionando como o esperado.</p>
                <p style="font-family: Arial, sans-serif; color: #fff;">🔒 <strong>Segurança em primeiro lugar!</strong> Eventualmente o sistema da API/bot, <strong>{env.BOT_NAME}</strong>, poderá enviar e-mails para você por segurança.</p>
                <p style="font-family: Arial, sans-serif; color: #fff;">👀 <strong>Fique atento!</strong>De tempos em tempos verifique a <strong>Caixa de Entrada</strong> ou <strong>Spam</strong> do seu email para ficar atualizado!</p>
            </td>
        </tr>
    </table>
'''
    email = default_document(env, main)

    return email


def critical_error(env, content: str) -> str:
    error = content.replace('\n', '<br>')
    main = f'''
    <table role="presentation" width="100%" style="padding: 20px; padding-top: 50px; text-align: center; margin-top: 50px; border-top: 2px #fff solid;">
        <tr style="background-color: #29434a;">
            <td>
                <h1 style="font-family: 'Courier New', monospace; margin-top: 40px; color: #ff9e9e; font-size: 20px;">Um erro crítico aconteceu no sistema</h1>
                <div style="background-color: #ff9e9e; width: min-content; padding: 10px; margin: auto; border: 1px #18282c solid; border-radius: 10px; display: inline-block;">
                    <h4 style="font-family: 'Courier New', monospace; color: #ffffff; margin-top: 0;">Traceback</h4>
                    <pre style="font-family: 'Courier New', Courier, monospace;">{error}</pre>
                </div>
               
                <p style="font-family: Arial, sans-serif; color: #ff9e9e;">⚠️ A execução sistema foi interrempida por conta de um <strong>erro crítico</strong>.</p>
                <p style="font-family: Arial, sans-serif; color: #ffffff;">ℹ️ Você poderá ver mais detalhes ou o processo que ocasionou o erro por meio dos <strong>logs</strong>.</p>
                <p style="font-family: Arial, sans-serif; color: #ffffff;">📌 Os logs estão acessíveis pela <strong>raíz do sistema</strong>, no diretório <strong>logs/</strong>.</p>
                <p style="font-family: Arial, sans-serif; color: #5df68d;">💡 Procure resolver o erro antes de executar o sistema novamente, evitando futuros problemas.</p>
        </tr>
    </table>
'''
    
    email = default_document(env, main)
    return email


def custom_email(env, subject: str, content: str) -> str:
    pass


'''Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'kd3dbljkqcbcbc' is not defined'''