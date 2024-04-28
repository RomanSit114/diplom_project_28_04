import pandas
from utils.mysql_client import execute_query


class Calculator:
    def handle_calculation_form(self, rooms):
        query = '''
            SELECT 
            rt.name as room_type,
            wt.type as work_type,
            wt.name as work_name,
            wt.price
            FROM work_at_room as war
            LEFT JOIN room_type rt ON rt.id = war.room_type_id
            LEFT JOIN work_types wt ON wt.id = war.work_type_id
        '''
        response = execute_query(query)
        work_params = pandas.DataFrame(response)

        with pandas.ExcelWriter("Смета.xlsx") as writer:
            for room in rooms:
                room_type = room['room_type']
                room_lenght = int(room['room_lenght']) # Длина
                room_width = int(room['room_width']) # Ширина
                room_height = int(room['room_height']) # Высота
                
                # Площадь потолка \ пола
                room_square = room_lenght * room_width
                # Периметр потолка \ пола
                room_perimeter = (room_width * 2) + (room_lenght * 2)
                # Площадь стен
                walls_square = ((room_lenght + room_width) * 2) * room_height
                

                rooms_df = []
                match room_type:
                    case 'Санузел':
                        df = pandas.DataFrame()

                        room_data = work_params[work_params['room_type'] == room_type]

                        for index, row in room_data.iterrows():
                            work_dataframe = pandas.DataFrame(
                                columns=["Вид работ", "Ед. измерения", "Объемы", "Стоимость, Руб", "Итого, Руб"],
                                data=[
                                    [
                                        row['work_type'],
                                        'м2',
                                        room_square,
                                        row['price'],
                                        room_square * row['price']
                                    ]
                                ]
                            )
                            
                            df = pandas.concat([df, work_dataframe])

                    case _:
                        df = pandas.DataFrame(
                        columns=["Вид работ", "Ед. измерения", "Объемы", "Стоимость, Руб", "Итого, Руб"],
                        data=[
                                ['Полы', '', 0,'',0,],
                                ['Стяжка', 'м2', room_square, '350', room_square * 350,],
                                ['Ламинат', 'м2', room_square, '550', room_square * 550,],
                                ['Плинтуса', 'МП', room_perimeter, '150', room_perimeter * 150,],

                                ['Стены', '', 0,'',0,],
                                ['Штукатурка', 'м2', walls_square, '500', walls_square * 500,],
                                ['Шпаклевка', 'м2', walls_square, '400', walls_square * 400,],
                                ['Обои', 'м2', walls_square, '250', walls_square * 250,],

                                ['Потолок', '', 0,'',0,],
                                ['Натяжной потолок', 'м2', room_square, '650', room_square * 650,],

                                ['Итого', '', 0,'',0,]
                            ]
                        )
                    
                total_row = df.sum(numeric_only=True)
                rooms_df.append(total_row)

                df.loc["Total"] = total_row
                df.to_excel(writer, sheet_name=room_type, index=False)

            total_df = pandas.concat(rooms_df)
            total_df.loc['Total'] = total_df.sum(numeric_only=True)
            total_df.to_excel(writer, sheet_name='Итого', index=False)
