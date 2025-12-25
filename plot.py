import psycopg2
import matplotlib.pyplot as plt
import time

REFRESH_INTERVAL = 2  

def main():
    try:
        conn = psycopg2.connect(dbname = "db_server", host= "localhost", user="postgres", password="postgres1234", port="5432")
        curs = conn.cursor()
        print("Подключение к БД установлено")
        
        plt.ion()
        fig, ax = plt.subplots(figsize=(10, 8))

        ax.set_title("Уровень сигнала RSRP в реальном времени")
        ax.set_xlabel("Долгота (Longitude)")
        ax.set_ylabel("Широта (Latitude)")
        ax.grid(True, alpha=0.3)
        
        scatter = None
        colorbar = None

        update_counter = 0
        
        print("График запущен. Для выхода закройте окно графика.")
        
        while plt.fignum_exists(fig.number): 
            try:
                curs.execute("""
                    SELECT lat, lon, rsrp
                    FROM info_abonent
                    WHERE lat IS NOT NULL 
                    AND lon IS NOT NULL 
                    AND rsrp IS NOT NULL
                """)
                rows = curs.fetchall()
                
                if rows:
                    lats = [float(r[0]) for r in rows]
                    lons = [float(r[1]) for r in rows]
                    rsrp = [float(r[2]) for r in rows]

                    ax.clear()
                    
                    scatter = ax.scatter(
                        lons,
                        lats,
                        c=rsrp,
                        cmap='jet',
                        vmin=-140,
                        vmax=-60,
                        s=60,
                        alpha=0.8,
                        edgecolors='white',
                        linewidth=0.5
                    )

                    ax.set_title(f"Уровень сигнала RSRP в реальном времени")
                    ax.set_xlabel("Долгота (Longitude)")
                    ax.set_ylabel("Широта (Latitude)")
                    ax.grid(True, alpha=0.3)

                    if colorbar is None:
                        colorbar = plt.colorbar(scatter, ax=ax)
                        colorbar.set_label("RSRP (dBm)")

                    update_counter += 1
                    print(f"Обновление #{update_counter}: {len(rows)} точек")
                else:
                    print("Нет данных для отображения")
                    
                fig.canvas.draw()
                fig.canvas.flush_events()

                time.sleep(REFRESH_INTERVAL)
                
            except KeyboardInterrupt:
                print("\nПрограмма остановлена пользователем")
                break
            except Exception as e:
                print(f"Ошибка при обновлении графика: {e}")
                time.sleep(REFRESH_INTERVAL)
                
    except psycopg2.Error as e:
        print(f"Ошибка подключения к БД: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
    finally:
        try:
            curs.close()
            conn.close()
            print("Подключение к БД закрыто")
        except:
            pass
        plt.ioff()
        plt.show()

if __name__ == "__main__":
    main()