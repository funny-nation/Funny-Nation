import { Client } from "discord.js"
import endpoint from "../endpoints.config"

(async ()=>{
  const client = new Client({
    intents:[]
})
client.on("ready", () => {
    console.log('logged in as ${client.user.tag}')
})

client.on("message", msg=>{
    if(msg.content === "plbsb") {
        msg.reply("yes it is")
    }

})
client.login(endpoint.BotToken)
})()