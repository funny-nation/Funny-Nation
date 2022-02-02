<div align="center">
    <h1>Funny Nation</h1>
</div>
<div align="center">
    <a href="https://discord.gg/uhAv4J4F7Z"><img src="https://img.shields.io/badge/Chat-Discord-7289da" alt="Our Discord"></a>
    <a href="https://github.com/plbin97/Funny-Nation/actions"><img src="https://github.com/plbin97/Funny-Nation/actions/workflows/main.yml/badge.svg"></a>
</div>

<div>
    <h3>About this</h3>
    <p>
        "Funny Nation" is a money-centric "Metaverse" within a Discord server. It is a Discord bot. There are games, activities, visual marriage, and virtual estate (channel) trade. 
    </p>
    <p>
        Anyone inside the Discord server could earn money via playing games, participating in activities, sending messages, speaking in the voice channel, streaming, and using the money they earned to play games and buy virtual estates (channels).
    </p>
    <p>
        If you could read Chinese, you could try this bot on those Discord servers: 
    </p>
    <ul>
        <li><a href="https://discord.gg/CynuYmyMxD">https://discord.gg/CynuYmyMxD</a></li>
        <li><a href="https://discord.gg/PAZy4QHZmb">https://discord.gg/PAZy4QHZmb</a></li>
    </ul>
    <p>
        Remember that you could only run that on one Discord server. This script does not support multi-servers. 
    </p>
</div>
<hr/>
<div>
    <h3>Get started</h3>
    <h4>Environment</h4>
    <p>Require <code>python 3.8+</code> and <code>MySQL 8.0+</code></p>
    <p>Install dependency</p>
    <pre><code>pip install -r requirements.txt</code></pre>
    <p>Create major configuration file</p>
    <pre><code>cp config.ini.example config.ini</code></pre>
    <p>Create migration configuration file</p>
    <pre><code>cp yoyo.ini.example yoyo.ini</code></pre>
    <p style="font-size: smaller">* You might need to manually install yoyo-migrations. </p>
    <p>Database migration</p>
    <pre><code>yoyo apply ./migrations</code></pre>
    <p style="font-size: smaller">* Remember to edit the configuration files and do the migrations before use.</p>
    <p>Start application</p>
    <pre><code>python main.py</code></pre>
    <hr/>
    <h3>Deploy your bot using Docker</h3>
    <p>Build container</p>
    <p style="font-size: smaller">* Remember that you should set up all your configuration files before building your container. </p>
    <pre><code>docker build -t myBot .</code></pre>
    <p>Run the container</p>
    <pre><code>docker run -d myBot</code></pre>
</div>
<hr/>
<div>
    <h3>Instructions for Use</h3>
    <p>You could find them in <code>docs/</code> folder. </p>
    <p>We only have a Simplified Chinese version. English version is currently not available yet. </p>
    <ul>
        <li><a href="docs/InstructionsForUse_SimplifiedChinese.md">Simplified Chinese</a></li>
    </ul>
</div>
<hr/>
<div>
    <h3>Chat</h3>
    <p>If you want to get involved in this project or gain any help, you could join this Discord server and message me. </p>
    <p><a href="https://discord.gg/uhAv4J4F7Z">https://discord.gg/uhAv4J4F7Z</a></p>
</div>
