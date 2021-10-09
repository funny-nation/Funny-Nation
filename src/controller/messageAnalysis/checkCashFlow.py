import sys
import os

sys.path.append(os.path.dirname(__file__) + '/../../model')
import cashFlowManagement


async def checkCashFlow(self, message, db):
    cashFlowData = cashFlowManagement.get10RecentCashflowsByUserID(db, message.author.id, None)
    messageSendBack = ''
    if cashFlowData is None:
        messageSendBack = '系统错误'
    else:
        messageSendBack += '最近的流水记录：\n'
        for cashFlow in cashFlowData:
            messageSendBack += f"{cashFlow[4].strftime('%Y-%m-%d %H:%M:%S')} - {cashFlow[3]} - {cashFlow[2] / 100} 元 \n---------------------\n"

    await message.channel.send(messageSendBack)


async def checkCashFlowWithFilter(self, message, db):
    filterMessage = message.content[6:]
    cashFlowData = cashFlowManagement.get10RecentCashflowsByUserID(db, message.author.id, filterMessage)
    messageSendBack = ''
    if cashFlowData is None:
        messageSendBack = '系统错误'
    else:
        if len(cashFlowData) == 0:
            messageSendBack += '未找到任何关于此的流水记录'
        else:
            
            messageSendBack += '找到的流水记录：\n'
            for cashFlow in cashFlowData:
                messageSendBack += f"{cashFlow[4].strftime('%Y-%m-%d %H:%M:%S')} - {cashFlow[3]} - {cashFlow[2] / 100} 元 \n---------------------\n"

    await message.channel.send(messageSendBack)