from datetime import datetime
import json
from ocr_test import image_ocr

# 정기등록 차량
members = {
    '37바4821': {
        'name': 'kim',
        'discount': 20,
    },
    '92가1034': {
        'name': 'park',
        'discount': 50,
    },
    '15나7749': {
        'name': 'lee',
        'discount': 0,
    }
}

# 기본 주차장
seats = [['♿', '♿', '♿', '⬛', '⬜', '🔋', '🔋', '🔋', '⬜', '⬜'],
         ['⬛', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛', '⬜', '⬜'],
         ['⬜', '⬛', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜'],
         ['⬜', '⬜', '⬛', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜']]

seat_types = [
    # A행: 0~2는 장애인, 5~7은 전기차
    ['D', 'D', 'D', 'N', 'N', 'E', 'E', 'E', 'N', 'N'],
    # B행
    ['N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N'],
    # C행
    ['N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N'],
    # D행
    ['N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N']
]

# 기본 주차장 자리 정보
occupied = {
    '25가1049': {
        'position': 'A4',
        'entrance': '2025-04-04 17:30'
    },
    '53바5029': {
        'position': 'B1',
        'entrance': '2025-07-15 18:30'
    },
    '10나5829': {
        'position': 'B8',
        'entrance': '2025-01-13 19:30'
    },
    '90바2819': {
        'position': 'D3',
        'entrance': '2025-05-12 20:30'
    },
    '92가1034': {
        'position': 'C2',
        'entrance': '2025-09-01 10:20'
    }
}

special_position = [0, 1, 2, 5, 6, 7]
disabled_position = [0, 1, 2]
electric_position = [5, 6, 7]


def alphabet_to_number(text):
    return ord(text.upper()) - 65


def is_eligible(row: int, col: int, kind: str) -> bool:
    """
    좌석 타입 대비 자격 확인.
    kind: 'd'(장애인), 'e'(전기차), 'n'(일반)
    """
    t = seat_types[row][col]
    if t == 'D':
        return kind == 'd'
    if t == 'E':
        return kind == 'e'
    return True  # 일반석은 누구나 가능


def print_seats(seats):
    print("[좌석 현황] (A~D 행, 1~10 열)")
    print("설명: ⬜ 일반 빈자리  ⬛ 점유중  ♿ 장애인 전용  🔋 전기차 전용")
    header = "     " + "  ".join(f"{i:>2}" for i in range(1, 11))
    print(header)
    for r, row in enumerate(seats):
        line = f"{chr(65+r)} | " + " ".join(f"{cell:>2}" for cell in row)
        print(line)
    print()


while True:
    run = input("시스템을 종료하기 위해서는 'exit'를 입력하세요: ").strip().upper()
    if run == 'EXIT':
        break

    print("===== 주차 시스템 =====")
    print("1: 입차")
    print("2: 출차")
    print("3: 멤버 계정")
    print("======================")
    in_out = input("메뉴를 선택하세요: ").strip()

    # =================입차==================
    if in_out == '1':
        print_seats(seats=seats)

        restart = 0
        desire_pos = input("원하는 주차 위치를 선택하세요(Ex: A5): ")
        desire_pos0 = alphabet_to_number(desire_pos[0])
        desire_pos1 = int(desire_pos[1])-1
        dis_or_elec = input("차량 유형 선택(d: 장애인, e: 전기차, n:일반): ").lower()
        if (desire_pos0 == 0) and (desire_pos1 in special_position):
            if dis_or_elec == 'n':
                print("해당 전용 좌석을 사용할 자격이 없습니다.")
                continue
            elif dis_or_elec == 'd':
                if desire_pos1 in electric_position:
                    print("해당 전용 좌석을 사용할 자격이 없습니다.")
                    continue
            elif dis_or_elec == 'e':
                if desire_pos1 in disabled_position:
                    print("해당 전용 좌석을 사용할 자격이 없습니다.")
                    continue

        if seats[desire_pos0][desire_pos1] == '⬛':
            print("선택한 자리는 이미 사용 중입니다.")
            empty_pos = []
            for i in range(len(seats)):
                for j in range(len(seats[i])):
                    if seats[i][j] != '⬛' and is_eligible(i, j, dis_or_elec):
                        empty_pos.append(f"{chr(i+65)}{j+1}")
                        if len(empty_pos) >= 3:
                            break
                if len(empty_pos) >= 3:
                    break
            print(f"추천 좌석: {empty_pos}")
            continue
        else:
            seats[desire_pos0][desire_pos1] = '⬛'
            print("해당 자리로 선택되었습니다.")

        # car_num = input("차량 번호를 입력하세요(Ex:12다1234): ")
        vehi_num = image_ocr()
        # in_time = input("Enter your entrance time(YYYY-MM-DD HH:MM): ")
        in_time = datetime.now().strftime("%Y-%m-%d %H:%M")

        occupied[vehi_num] = {
            'position': desire_pos,
            'entrance': in_time
        }
        print_seats(seats=seats)
        print(json.dumps(occupied, indent=2, ensure_ascii=False))

    # =====================출차=====================
    elif in_out == '2':
        print(json.dumps(occupied, indent=2, ensure_ascii=False))
        car_num = input("차량 번호를 입력하세요(Ex:12다1234): ")
        if car_num not in occupied:
            print("등록된 주차 기록이 없습니다.")
            continue
        print(occupied[car_num])

        # out_time = input("Enter your out time(YYYY-MM-DD HH:MM): ")
        out_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        in_dt = datetime.strptime(
            occupied[car_num]['entrance'], "%Y-%m-%d %H:%M")
        out_dt = datetime.strptime(out_time, "%Y-%m-%d %H:%M")
        diff = out_dt - in_dt

        total_30mins, _ = divmod(diff.total_seconds(), 1800)
        if car_num in members:
            discount = members[car_num]['discount']
        else:
            discount = 100

        total_price = (total_30mins)*10000*(discount*0.01)
        print(f"Your exit time is {out_dt}")
        print(f"Your total fee is {int(total_price)}won.")

        out_position = occupied[car_num]['position']
        out_pos1 = alphabet_to_number(out_position[0])
        out_pos2 = int(out_position[1])-1

        if out_pos1 == 0:
            if out_pos2 in disabled_position:
                seats[out_pos1][out_pos2] = '♿'
            elif out_pos2 in electric_position:
                seats[out_pos1][out_pos2] = '🔋'
            else:
                seats[out_pos1][out_pos2] = '⬜'
        else:
            seats[out_pos1][out_pos2] = '⬜'

        del occupied[car_num]
        print_seats(seats=seats)
        
    # ================정기차량 등록======================
    elif in_out == '3':
        print(json.dumps(members, indent=2, ensure_ascii=False))
        new_name = input("이름을 입력하세요: ")
        new_car = input("차량 번호를 입력하세요(Ex:12다1234): ")
        if new_car in members:
            if new_name in members[new_car]['name']:
                delete_member = input("등록 정보를 삭제하시겠습니까?(Y/N): ").upper()
                if delete_member == 'Y':
                    del members[new_car]
                    print(f" {new_car} 등록 정보가 삭제되었습니다.")
                    continue
                else:
                    continue

        new_discount = input("할인을 위한 유형을 선택하세요(1: 국가유공자, 2: 다자녀, 3: 일반): ")

        if new_discount == '1':
            dis_rate = 20
        elif new_discount == '2':
            dis_rate = 50
        else:
            dis_rate = 0

        members[new_car] = {
            'name': new_name,
            'discount': dis_rate
        }
        print(json.dumps(members, indent=2, ensure_ascii=False))

    else:
        continue
