import psutil
import telebot
import os

API_TOKEN = os.environ.get("SYSINFOBOT_KEY")
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['info'])
def send_info(message):
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    gpu_info = psutil.sensors_temperatures()
    
    response = f"CPU Usage: {cpu_percent}%\n"
    response += f"Memory Total: {memory.total / (1024**3):.2f} GB\n"
    response += f"Memory Used: {memory.used / (1024**3):.2f} GB\n"

    if 'coretemp' in gpu_info:
        for temp in gpu_info['coretemp']:
            response += f"GPU Temperature: {temp.current}°C\n"

    bot.reply_to(message, response)

@bot.message_handler(commands=['top'])
def send_top_processes(message):
    processes = list(psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_info']))
    top_processes = sorted(processes, key=lambda x: x.info['cpu_percent'], reverse=True)[:5]

    response = "Top 5 CPU Consuming Processes:\n"
    for idx, process in enumerate(top_processes, start=1):
        response += f"{idx}. {process.info['name']} - CPU: {process.info['cpu_percent']}%, Memory: {process.info['memory_info'].rss / (1024**2):.2f} MB\n"

    bot.reply_to(message, response)

bot.polling()
