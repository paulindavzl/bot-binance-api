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


def error_log(env, content: dict) -> str:
    pass


def custom_email(env, subject: str, content: str) -> str:
    pass
