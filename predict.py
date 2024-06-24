import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error as mse
from sklearn.preprocessing import PolynomialFeatures
from datetime import date
from dateutil.relativedelta import relativedelta
import joblib
import openpyxl

st.title("команда НЕайтишники")
st.header("краткосрочное потребление газа в регионах")

region = st.selectbox("Регион", range(1, 64))
longivity = st.selectbox("На сколько нужно сделать расчет", range(1, 8))
temperature = st.text_input("Температура", help="Введите температуру одной строкой, разделяя значения пробелами")
day_type = st.text_input("Тип дня", help="Введите тип дня одной строкой, разделяя значения пробелами (по умолчанию - 0)")

# Обработка данных
if st.button("Рассчитать"):
    
    reg = int(region) - 1
    long = int(longivity)

    if temperature != "":
        temp = list(map(float, temperature.split()))

        if len(temp) == long:

            if day_type != "":
                days = list(map(int, day_type.split()))
            else:
                days = [0] * long

            data = np.array([list(i) for i in zip(temp, days)])
            features = PolynomialFeatures(3).fit_transform(data)

            print(features)

            model = joblib.load(f"linears\\linear{reg}.joblib")


            forecast = model.predict(features)

            st.write(f"Прогноз потребления на близжайшие {long} дней:")
            for i in range(1, long + 1):
                st.write(f"{date.today() + relativedelta(days=i)}: {round(forecast[i-1], 2)} кубометров газа")

            dates = [date.today() + relativedelta(days=i) for i in range(1, len(forecast) + 1)]

            # Преобразование дат в формат matplotlib
            dates = [d.strftime('%Y-%m-%d') for d in dates]  # Преобразование в строку 

            # Построение графика
            fig, ax = plt.subplots()  # Создаем фигуру и ось
            ax.plot(dates, forecast)  # Построение графика
            ax.set_xlabel("Дата")  # Подпись оси X
            ax.set_ylabel("Потребление Газа")  # Подпись оси Y
            ax.set_title("График потребления газа по датам")  # Заголовок

        

            st.pyplot(fig)  # Отображение графика в Streamlit

            with open("conf_ints.txt", "r") as f:
                s = f.readlines()[reg]
                conf = list(map(float, s.split()))
            
            st.write(f"Доверительный интервал прогноза: от {round(conf[0], 2)} до {round(conf[1], 2)} кб. газа")

            try:
                new = [[j[0], j[1], j[2][0], j[2][1]] for j in zip(dates, forecast, data)]

                
                workbook = openpyxl.load_workbook(f'Данные по регионам\\region {reg}.xlsx')
                sheet = workbook.active

                for row in new:
                    sheet.append(row)

                                
                workbook.save(f"Данные по регионам\\region {reg}.xlsx")

                st.write("Прогноз сохранен!")
            except:
                st.write("Что-то пошло не так и прогноз не сохранился...")
        else:
            st.write("Убедитесь, что вы корректно ввели данные!")

    else:
        st.write("Убедитесь, что вы корректно ввели данные!")



        
