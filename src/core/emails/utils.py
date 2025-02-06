def default_document(env, main) -> str:
    html = f'''
<!DOCTYPE html>
<html lang="en">
{head(env)}
<body style="box-sizing: border-box; margin: 0; padding: 10px; background-color: #18282c; width: 100%;">
    {header(env)}
    {main}
</body>
</html>
'''

    return html


def head(env) -> str:
    html = f''' 
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{env.BOT_NAME}</title>
</head>
'''
    return html


def header(env) -> str:
    html = f''' 
    <table role="presentation" width="99%" style="text-align: center; background-color: #29434a;">
        <tr>
            <td>
                <label>
                    <a href="{env.GITHUB}" style="text-decoration: none;">
                        <img src="https://img.icons8.com/?size=100&id=106564&format=png&color=000000" alt="GitHub" style="width: 15%;">
                        <p style="color: #fff; font-size: 65%; font-family: Verdana, sans-serif;">GitHub Admin</p>
                    </a>
                </label>
            </td>

            <td>
                <h1 style="font-family: 'Courier New', monospace; color: #131414">{env.BOT_NAME}</h1>
                <p style="color: #fff; font-family: 'Courier New', monospace; font-size: 80%;">Sua API/bot de trade automático na <a href="https://binance.com/" style="text-decoration: none; color: #fff;">Binance</a></p>
            </td>

            <td>
                <label>
                    <a href="https://github.com/paulindavzl/bot-binance-api" style="text-decoration: none;">
                        <img src="https://img.icons8.com/?size=100&id=2PelG5XP5nN5&format=png&color=000000" alt="GitHub" style="width: 15%;">
                        <p style="color: #fff; font-size: 65%; font-family: Verdana, sans-serif;">GitHub API</p>
                    </a>
                </label>
            </td>
        </tr>
    </table>
'''
    return html