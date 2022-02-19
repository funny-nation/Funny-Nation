from discord import Client, Message, embeds

async def test(self: Client, message: Message):
    embed = embeds.Embed(title="test",
                          url="https://www.google.com/search?q=%E6%B1%82%E6%9E%81%E9%99%90&oq=&aqs=chrome.4.69i59i450l8.29966237j0j15&sourceid=chrome&ie=UTF-8",
                          description="test")
    embed.set_author(name="nawu",
                     url="https://www.google.com/search?q=%E6%B1%82%E6%9E%81%E9%99%90&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjc_oWYzu_1AhV1jIkEHRKZBQcQ_AUoAXoECAEQAw&biw=1536&bih=714&dpr=1.25#imgrc=rzz00wvMdR8kPM",
                     icon_url="https://www.google.com/search?q=%E6%B1%82%E6%9E%81%E9%99%90&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjc_oWYzu_1AhV1jIkEHRKZBQcQ_AUoAXoECAEQAw&biw=1536&bih=714&dpr=1.25#imgrc=rzz00wvMdR8kPM")
    embed.set_thumbnail(
        url="https://www.google.com/search?q=%E6%B1%82%E6%9E%81%E9%99%90&oq=&aqs=chrome.4.69i59i450l8.29966237j0j15&sourceid=chrome&ie=UTF-8")
    await message.send(embed=embed)