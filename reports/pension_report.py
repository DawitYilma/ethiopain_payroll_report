
from datetime import date
from odoo import models
import base64
import io
from odoo.modules.module import get_module_resource


class Pension(models.AbstractModel):
    _name = 'report.payroll_report.report_payroll_pension'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        col = workbook.add_format({'font_size': 10, 'align': 'vcenter', 'border': 1})
        col0 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        col_wrap = workbook.add_format({'font_size': 10, 'text_wrap': True, 'align': 'vcenter', 'border': 1})
        col0_wrap = workbook.add_format({'font_size': 14, 'text_wrap': True, 'align': 'vcenter', 'bold': True})
        col1 = workbook.add_format({'font_size': 10, 'align': 'vcenter', 'bold': True, 'border': 1})
        cell_format = workbook.add_format({'font_size': 10, 'align': 'vcenter', 'bg_color': 'B3B3B3', 'border': 1})
        col2 = workbook.add_format({'font_size': 10, 'align': 'vcenter', 'border': 1})
        col3 = workbook.add_format({'font_size': 10, 'align': 'vcenter', 'border': 0})
        date_format = workbook.add_format({'num_format': 'mmmm d yyyy', 'border': 1})
        sheet = workbook.add_worksheet("Pension")

        sheet.set_column(0, 0, 8)
        sheet.set_column(1, 1, 20)
        sheet.set_column(2, 2, 20)
        sheet.set_column(3, 3, 17)
        sheet.set_column(4, 4, 17)
        sheet.set_column(5, 5, 17)
        sheet.set_column(6, 6, 11)
        sheet.set_column(7, 7, 17)
        sheet.set_column(8, 8, 17)
        sheet.set_column(9, 9, 17)

        image_path = get_module_resource('payroll_report', 'static/src/img', 'pension.png')
        image_file = open(image_path, 'rb')
        image_data = io.BytesIO(image_file.read())
        sheet.insert_image(0, 0, 'incometax_image.png', {'image_data': image_data, 'x_scale': 0.7, 'y_scale': 0.7})

        sheet.write(6, 2, 'ክፍል - 1 የጡረታ መዋጮውን የሚከፍለው ድርጅት ዝርዝር መረጃ', col0)
        if lines.company_id.owner.name != False:
            sheet.merge_range(7, 0, 8, 2, 'የድርጅቱ ስም: ' + str(lines.company_id.owner.name), col)
        else:
            sheet.merge_range(7, 0, 8, 2, 'የድርጅቱ ስም: ', col)
        sheet.merge_range(7, 3, 8, 3, '3. የድርጅቱ የግብር ከፋይ መለያ ቁጥር: ' + str(lines.company_id.vat), col_wrap)
        sheet.merge_range(7, 4, 8, 4, '4. የግብር ሂሣብ ቁጥር', col)
        today = date.today()
        month = today.strftime("%B")
        year = today.strftime("%Y")
        sheet.merge_range(7, 5, 7, 7, 'የክፍያ ጊዜ', col)
        sheet.write(8, 5, month, col)
        sheet.merge_range(8, 6, 8, 7, year, col)
        sheet.merge_range(7, 8, 8, 9, ' ', col)
        sheet.merge_range(9, 0, 11, 0, '2a. ክልል: ' + str(lines.company_id.state_id.name), col)
        sheet.write(9, 1, '2b. ዞን/ክፍለ  ከተማ: ', col3)
        sheet.write(10, 1, lines.company_id.city, col3)
        sheet.write(11, 1, ' ', col3)
        sheet.merge_range(9, 2, 11, 2, ' ', col)
        sheet.merge_range(9, 3, 9, 7, '5. የጡረታ መዋጮ ገቢ ሰብሳቢ መ/ቤት ሰም', col3)
        sheet.merge_range(10, 3, 10, 7, 'የኢትዮጵያ ገቢዎችና ጉምሩክ ባለስልጣን አነስተኛ ግብር ከፋዮች ቅርንጫፍ ፅ/ቤት፤', col3)
        sheet.merge_range(11, 3, 11, 7, 'የግል ድርጅት ሠራተኞች የጡረታ መዋጮ', col3)
        sheet.merge_range(12, 0, 13, 0, '2c. ወረዳ', col)
        sheet.merge_range(12, 1, 13, 1, '2d. ቀበሌ/ገበሬ ማህበር', col)
        sheet.merge_range(12, 2, 13, 2, '2e. የቤት ቁጥር', col)
        sheet.merge_range(12, 3, 13, 4, '6. የስልክ ቁጥር: ' + str(lines.company_id.phone), col)
        sheet.merge_range(12, 5, 13, 7, '7. ፋክስ ቁጥር', col)
        sheet.merge_range(9, 8, 9, 9, 'የሰነድ ቁጥር (ለቢሮ አገልግሎት ብቻ)', col)
        sheet.merge_range(10, 8, 10, 9, ' ', col)
        sheet.merge_range(11, 8, 11, 9, ' ', col)
        sheet.merge_range(12, 8, 12, 9, ' ', col)
        sheet.merge_range(13, 8, 13, 9, ' ', col)

        topic = ['u) ተራ.ቁ.', 'ለ) የቋሚ ሠራተኛው የግብር ከተፋየ መለያ ቁጥር (TIN)', 'ሐ) የሠራተኛው ስም፣ የአባት ስም እና የአያት ስም',
                 'መ) የተቀጠሩበት ቀን/ወር/ዓ.ም', 'ሠ) የወር ደመወዝ /ብር/', 'ረ) የሠራተኛው መዋጮ መጠን --7-%/ብር/',
                 'ሰ) የአሰሪው መዋጮ መጠን 11---%/ብር/', 'ሸ) በአሰሪው የሚገባ ጥቅል መዋጮ -18--%ብር(ረ+ሰ)']

        sheet.write(14, 4, 'ሠንጠረዥ -2 የማስታወቂያ ዝርዝር መረጃ', col0)
        for line in range(len(topic)):
            sheet.merge_range(15, line, 16, line, topic[line], col_wrap)
        sheet.merge_range(15, 8, 16, 9, 'ፊርማ', col)
        add_lis = [0, 0, 0, 0]
        line_count = 1
        col_count = 1
        row_count = 17
        bas_sal = 0
        bas_fir = 0
        bas_sec = 0
        tot = 0
        for payslip in lines:
            if payslip.contract_id.name != False:
                for line in payslip.line_ids:
                    sheet.set_row(row_count, 20)
                    if line.name == "Basic Salary":
                        bas_sal = line.amount
                        bas_fir = bas_sal * 0.07
                        bas_sec = bas_sal * 0.11
                        tot = bas_fir + bas_sec
                sheet.write(row_count, 0, line_count, col2)
                sheet.write(row_count, 1, payslip.employee_id.tin_number, col2)
                sheet.write(row_count, 2, payslip.employee_id.name, col2)
                sheet.write_datetime(row_count, 3, payslip.contract_id.date_start, date_format)
                sheet.write(row_count, 4, bas_sal, col2)
                add_lis[0] += bas_sal
                sheet.write(row_count, 5, bas_fir, col2)
                add_lis[1] += bas_fir
                sheet.write(row_count, 6, bas_sec, col2)
                add_lis[2] += bas_sec
                sheet.write(row_count, 7, tot, col2)
                add_lis[3] += tot
            line_count += 1
            col_count += 1
            row_count += 1
        for line in range(len(add_lis)):
            if add_lis[line] != 0:
                sheet.write(row_count, 4 + line, add_lis[line], col1)
            else:
                sheet.write(row_count, 4 + line, ' ', col1)
        sheet.write(row_count, 3, 'ከአባሪ ቅጾች የመጣ ድምር', col)

        sheet.write(row_count + 2, 0, 'ክፍል 3 - የወሩ የተጠቃለለ ሂሣብ', col0)
        sheet.write(row_count + 3, 0, 10, col)
        sheet.write(row_count + 4, 0, 20, col)
        sheet.write(row_count + 5, 0, 30, col)
        sheet.write(row_count + 6, 0, 40, col)
        sheet.write(row_count + 7, 0, 50, col)
        sheet.merge_range(row_count + 3, 1, row_count + 3, 2, 'በዚህ ወር ደመወዝ የሚከፈላቸው የሠራተኞች ብዛት', col)
        sheet.write(row_count + 3, 3, line_count - 1, col)
        sheet.write(row_count + 3, 5, 'የሠራተኛው/ስም የአባት ስምና የአያት ስም/', col_wrap)
        sheet.merge_range(row_count + 3, 7, row_count + 3, 8, 'የተከፈለበት ቀን', col)
        sheet.write(row_count + 3, 9, ' ', col)
        sheet.merge_range(row_count + 4, 1, row_count + 4, 2, 'የወሩ ጠቅላላ የሠራተኞች ደመወዝ (ከላይ ካለው ከሠንጠረዥ (ሠ))', col)
        sheet.write(row_count + 4, 3, add_lis[0], col)
        sheet.write(row_count + 4, 5, ' ', col)
        sheet.merge_range(row_count + 4, 7, row_count + 4, 8, 'የደረሰኝ ቁጥር ', col)
        sheet.write(row_count + 4, 9, ' ', col)
        sheet.merge_range(row_count + 5, 1, row_count + 5, 2, 'የወሩ ጠቅላላ የሰራተኞች መዋጮ መጠን (ከላይ ካለው ከሠንጠረዥ (ረ))', col)
        sheet.write(row_count + 5, 3, add_lis[1], col)
        sheet.write(row_count + 5, 5, ' ', col)
        sheet.merge_range(row_count + 5, 7,row_count + 5, 8, 'የገንዘብ ልክ ', col)
        sheet.write(row_count + 5, 9, ' ', col)
        sheet.merge_range(row_count + 6, 1, row_count + 6, 2, 'የወሩ ጠቅላላ የአሰሪው መዋጮ መጠን (ከላይ ካለው ከሠንጠረዥ (ሰ))', col)
        sheet.write(row_count + 6, 3, add_lis[2], col)
        sheet.write(row_count + 6, 5, ' ', col)
        sheet.merge_range(row_count + 6, 7, row_count + 6, 8, 'ቼክ ቁጥር ', col)
        sheet.write(row_count + 6, 9, ' ', col)
        sheet.merge_range(row_count + 7, 1, row_count + 7, 2, 'የወሩ ጠቅላላ የመዋጮ መዋጮ መጠን (ከላይ ካለው ከሠንጠረዥ (ሸ))', col)
        sheet.write(row_count + 7, 3, add_lis[3], col)
        sheet.write(row_count + 7, 5, ' ', col)
        sheet.merge_range(row_count + 7, 7, row_count + 7, 8, 'የገንዘብ ተቀባይ ፊርማ', col)
        sheet.write(row_count + 7, 9, ' ', col)

        sheet.write(row_count + 9, 0, 'ክፍል - 5 የትክክለኛነት ማረጋገጫ', col0)
        sheet.merge_range(row_count + 10, 0, row_count + 10, 2, 'ከላይ የተገለፀው ማስታቂያና የተሰጠው መረጃ በሙሉ', col)
        sheet.merge_range(row_count + 11, 0, row_count + 11, 2, 'የተሟላና ትክክለኛ መሆኑን አረጋግጣለሁ፡፡ ትክክለኛ ያልሆነ ', col3)
        sheet.merge_range(row_count + 12, 0, row_count + 12, 2, 'መረጃ ማቅረብ በግብር ሕጐችም ሆነ በወንጀለኛ መቅጫ ሕግ', col3)
        sheet.merge_range(row_count + 13, 0, row_count + 13, 2, 'የሚያስቀጣ መሆኑን እገነዘባለሁ፡፡', col)
        sheet.merge_range(row_count + 10, 3, row_count + 10, 5, 'የድርጅቱ/ሕጋዊ  ወኪሉ', col)
        sheet.merge_range(row_count + 11, 3, row_count + 11, 5, 'ስም ------------------------------------', col)
        sheet.merge_range(row_count + 12, 3, row_count + 12, 5, 'ፊርማ  ------------------------------', col)
        sheet.merge_range(row_count + 13, 3, row_count + 13, 5, 'ቀን ---------------------------------', col)
        sheet.merge_range(row_count + 10, 6, row_count + 10, 9, 'የግብር ሥልጣን', col)
        sheet.merge_range(row_count + 11, 6, row_count + 11, 9, 'ስም ------------------------------------', col)
        sheet.merge_range(row_count + 12, 6, row_count + 12, 9, 'ፊርማ  ------------------------------', col)
        sheet.merge_range(row_count + 13, 6, row_count + 13, 9, 'ቀን ---------------------------------', col)

        sheet.write(row_count + 15, 0, 'Ethiopian Revenue & Customs Authority (as of 8---/5/2011', col1)
        sheet.write(row_count + 16, 0, 'ማሳሰቢያ፡- የሠራኞችን ዝርዝር መሙያ ተጨማሪ ቦታ ካስፈለግዎት የተጨማሪ ማስታወቂያ ቅፁን ይጠቀሙ', col1)

        sheet.set_row(6, 20)

        sheet.set_row(7, 40)
        sheet.set_row(8, 20)
        sheet.set_row(9, 20)
        sheet.set_row(10, 20)
        sheet.set_row(11, 20)
        sheet.set_row(12, 20)
        sheet.set_row(13, 20)
        sheet.set_row(14, 20)
        sheet.set_row(15, 20)
        sheet.set_row(16, 20)
        for count in range(17):
            if count > 1:
                sheet.set_row(row_count + count, 20)





