const Discord = require("discord.js")
const client = new Discord.Client()

client.on("ready", () => {
    console.log('logged in as &{client.user.tag}')
})

client.on("message", msg=>{
    if(msg.content === "plbsb") {
        msg.reply("yes it is")
    }

})

client.login(process.env.TOKEN)