

import MetaTrader5 as mt5
import pandas as pd 
import threading as th
import time
import datetime

import math
import pytz
import numpy as np

print('run')


tehran_timezone = pytz.timezone('Asia/Tehran')

df_pross = pd.DataFrame(columns= ['time' ,  'pros' , 'sum_trade' , 'balance'])

def round_up(number, precision):

  return math.ceil(number * (10**precision)) / (10**precision)


def init():
    # mt5.initialize(path = r"C:\Program Files\LiteFinance MT5 real\terminal64.exe")
    # mt5.login(6920086 , password= 'Mahdi1400@' , server= 'LiteFinance-MT5-Live')

    init = mt5.initialize(path=r"C:\Program Files\LiteFinance MT5 2\terminal64.exe")
    mt5.login(89373537, password='Mahdi1400@', server='LiteFinance-MT5-Demo')


def info():

    account_info=mt5.account_info()

    balance = account_info.balance
    equity  = account_info.equity
    profit  = account_info.profit
    
    return balance , equity , profit
    

def round_up(number, precision):

  return math.ceil(number * (10**precision)) / (10**precision)


def buy(symbol , lot , tp_ , sl_ , comment ):

    
    
    tp = abs(mt5.symbol_info_tick(symbol).bid + tp_ ) 
    sl = abs(mt5.symbol_info_tick(symbol).ask - sl_ ) 
    pos = mt5.ORDER_TYPE_BUY



    lot = round_up(lot, 2)
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).bid
    deviation = 100
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type":  pos ,
        "price": price,
        "deviation": deviation,
        "magic": 234002,
        "comment": comment,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK ,
    }
     
    # send a trading request
    result = mt5.order_send(request)
    print(result)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        return ("failed . order_send failed, retcode={} {}".format(result.retcode ,request )) , False
        
    if result.retcode == 10009 :
        return result
    # if result:
    #     if result.retcode != mt5.TRADE_RETCODE_DONE:
    #         print("2. order_send failed, retcode={}".format(result.retcode))
    #         # request the result as a dictionary and display it element by element
    #         result_dict=result._asdict()
    #         for field in result_dict.keys():
    #             print("   {}={}".format(field,result_dict[field]))
    #             # if this is a trading request structure, display it element by element as well
    #             if field=="request":
    #                 traderequest_dict=result_dict[field]._asdict()
    #                 for tradereq_filed in traderequest_dict:
    #                     print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))



def sell(symbol , lot , tp_ , sl_, comment ):

    
    
    tp = abs(mt5.symbol_info_tick(symbol).ask - tp_  ) 
    sl = abs(mt5.symbol_info_tick(symbol).bid + sl_   ) 
    # tp = abs(mt5.symbol_info_tick(symbol).ask - tp_ -  (tp_ / 2 ) ) 
    # sl = abs(mt5.symbol_info_tick(symbol).bid + sl_ - ( tp_ / 2) ) 
    pos = mt5.ORDER_TYPE_SELL



    lot = round_up(lot, 2)
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).bid
    deviation = 100
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type":  pos ,
        "price": price,
        "deviation": deviation,
        "magic": 234002,
        "comment":  comment,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK ,
    }
     
    # send a trading request
    result = mt5.order_send(request)
    print(result)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        
        return ("failed . order_send failed, retcode={} {}".format(result.retcode ,request )) , False
        
    if result.retcode == 10009 :
        return result
    # if result:
    #     if result.retcode != mt5.TRADE_RETCODE_DONE:
    #         print("2. order_send failed, retcode={}".format(result.retcode))
    #         # request the result as a dictionary and display it element by element
    #         result_dict=result._asdict()
    #         for field in result_dict.keys():
    #             print("   {}={}".format(field,result_dict[field]))
    #             # if this is a trading request structure, display it element by element as well
    #             if field=="request":
    #                 traderequest_dict=result_dict[field]._asdict()
    #                 for tradereq_filed in traderequest_dict:
    #                     print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))


def close(ticket):
    
    
    
    def close_position(position):
        try:
            tick = mt5.symbol_info_tick(position.symbol)

            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "position": position.ticket,
                "symbol": position.symbol,
                "volume": position.volume,
                "type": mt5.ORDER_TYPE_BUY if position.type == 1 else mt5.ORDER_TYPE_SELL,
                "price": tick.ask if position.type == 1 else tick.bid,  
                "deviation": 100,
                "magic": 234002,
                "comment": "Gu",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_FOK ,
            }

            result = mt5.order_send(request)
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                result ("Close failed . order_send failed, retcode={} {}".format(result.retcode ,request ))
                return False
            if result.retcode == 10009 :
                return True
        except Exception as e:
            print(f'Close : Eror in def close {e}')

    positions = mt5.positions_get()
    for position in positions:
        # print(position)
        
        if position.ticket == ticket :
            try:
                
                doit =  close_position(position)
                return doit

            except Exception as e:
                print(f'Clsoe : Eror for Clsoe {e}')


def close_(ticket , volume , comment):
    comment = str(comment)
    volume = round(volume , 2)
    
    def close_position(position , volume , comment):
        try:
            tick = mt5.symbol_info_tick(position.symbol)

            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "position": position.ticket,
                "symbol": position.symbol,
                "volume": volume,
                "type": mt5.ORDER_TYPE_BUY if position.type == 1 else mt5.ORDER_TYPE_SELL,
                "price": tick.ask if position.type == 1 else tick.bid,  
                "deviation": 100,
                "magic": 234002,
                "comment": comment,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_FOK ,
            }

            result = mt5.order_send(request)
            # if result.retcode != mt5.TRADE_RETCODE_DONE:
            #     result ("Close failed . order_send failed, retcode={} {}".format(result.retcode ,request ))
            #     return False
            print(result , request)
        except Exception as e:
            print(f'Close : Eror in def close 219 {e}')

    positions = mt5.positions_get()
    for position in positions:
        # print(position)
        
        if position.ticket == ticket :
            try:
                
                close_position(position , volume , comment)
                return 'clsoe'
                time.sleep(0.1)

            except Exception as e:
                print(f'Clsoe : Eror for Clsoe 233 {e}')
            time.sleep(0.05)


def order_close(symbol):
    orders=mt5.orders_get(symbol = symbol)
    

    if orders :
        request = {

            'action' : mt5.TRADE_ACTION_REMOVE , 
            'order'  : mt5.orders_get(symbol = symbol)[0].ticket

        }
        
        result =  mt5.order_send(request)
        if result is None:
            print("No orders with group=\"*GBP*\", error code={}".format(mt5.last_error()))
        else:

            if result.retcode == 10009 :

                return  True


def close_nith():
    while True:
        time.sleep(0.2)
        try :
            dic_tick = {}
            jam = 0
            
            positions = mt5.positions_get()
            for position in positions:
                # print(position)
                
                dic_tick[position.ticket] = position.profit
                jam = jam + position.profit
            print('nith close' , jam)
            if jam >= 0 :
                for i in dic_tick:
                    time.sleep(0.2)
                    close(i)
                    break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)


def tradeone():
    # while True:
        try:
            # if len(mt5.positions_get()) == 0 :

                one_eur = buy('EURGBP_o' , 0.01 , 0.05 , 0.05 , 'one')            
              
                one_gbp = buy('GBPUSD_o' , 0.01 , 0.05 , 0.05 , 'one')

                one_eur_gbp = sell('EURUSD_o' , 0.01 , 0.05 , 0.05 , 'one')




                return one_gbp , one_eur_gbp , one_eur 
        except Exception as e:
            print(f"Error: {e}")


def tradetow():
        try:
            # if len(mt5.positions_get()) == 0 :
       
                tow_eur_gbp = sell('EURGBP_o' , 0.01 , 0.05 , 0.05 , 'tow')
              
                tow_gbp = sell('GBPUSD_o' , 0.01 , 0.05 , 0.05 , 'tow')

                tow_eur = buy('EURUSD_o' , 0.01 , 0.05 , 0.05 , 'tow')




                return  tow_gbp , tow_eur ,  tow_eur_gbp
        except Exception as e:
            print(f"Error: {e}")


def profit(one_gbp , tow_gbp , tow_eur , one_eur_gbp , one_eur , tow_eur_gbp):

    while True:
        try:
            time.sleep(0.01)
            if len(mt5.positions_get(one_gbp.order)) == 0 and len(mt5.positions_get(one_eur.order)) == 0 and len(mt5.positions_get(one_eur_gbp.order)) == 0 :
                one_gbp ,  one_eur_gbp  , one_eur  = tradeone()
            else:
                profit_one = mt5.positions_get( ticket =  one_gbp.order)[0].profit + mt5.positions_get( ticket =  one_eur.order)[0].profit + mt5.positions_get( ticket =  one_eur_gbp.order)[0].profit
                if profit_one >= 4 :
                    close(one_gbp.order)
                    close(one_eur.order)
                    close(one_eur_gbp.order)
                    break

            if len(mt5.positions_get(tow_gbp.order)) == 0 and len(mt5.positions_get(tow_eur.order)) == 0 and len(mt5.positions_get(tow_eur_gbp.order)) == 0 :
                tow_gbp ,  tow_eur      , tow_eur_gbp   = tradetow()
            else:
                profit_tow = mt5.positions_get( ticket =  tow_gbp.order)[0].profit + mt5.positions_get( ticket =  tow_eur.order)[0].profit + mt5.positions_get( ticket =  tow_eur_gbp.order)[0].profit
                if profit_tow >= 4 :
                    close(tow_gbp.order)
                    close(tow_eur.order)
                    close(tow_eur_gbp.order)
                    break

            



        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)


def write_to_csv(filename, data):
    df = pd.DataFrame(data, columns=['time', 'one', 'tow'])
    try:
        existing_df = pd.read_csv(filename)
        df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        pass
    df.to_csv(filename, index=False)




def profit_tow(one_gbp , tow_gbp , tow_eur , one_eur_gbp , one_eur , tow_eur_gbp):

    while True:
        try:

            
            profit_one = mt5.positions_get( ticket =  one_gbp.order)[0].profit + mt5.positions_get( ticket =  one_eur.order)[0].profit + mt5.positions_get( ticket =  one_eur_gbp.order)[0].profit
            profit_tow = mt5.positions_get( ticket =  tow_gbp.order)[0].profit + mt5.positions_get( ticket =  tow_eur.order)[0].profit + mt5.positions_get( ticket =  tow_eur_gbp.order)[0].profit

            
            data = [[datetime.datetime.now(), profit_one, profit_tow]]
            write_to_csv('trade_arbit.csv', data)



        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)

init()

one_gbp ,  one_eur_gbp  , one_eur       = tradeone()
tow_gbp ,  tow_eur      , tow_eur_gbp   = tradetow()

profit_tow(one_gbp , tow_gbp , tow_eur , one_eur_gbp , one_eur , tow_eur_gbp)
























