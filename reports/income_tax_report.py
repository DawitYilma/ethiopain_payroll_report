
from datetime import date
from odoo import models
import base64
import io
from odoo.modules.module import get_module_resource


class IncomeTax(models.AbstractModel):
    _name = 'report.payroll_report.report_payroll_income'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        col = workbook.add_format({'font_size': 10, 'align': 'vcenter', 'border': 1})
        col_wrap = workbook.add_format({'font_size': 10, 'text_wrap': True, 'align': 'vcenter', 'border': 1})
        col0_wrap = workbook.add_format({'font_size': 14, 'text_wrap': True, 'align': 'vcenter', 'bold': True})
        col0 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        col1 = workbook.add_format({'font_size': 10, 'align': 'vcenter', 'bold': True, 'border': 1})
        cell_format = workbook.add_format({'font_size': 10, 'text_wrap': True, 'align': 'vcenter', 'bg_color': 'B3B3B3', 'border': 1})
        col2 = workbook.add_format({'font_size': 10, 'align': 'vcenter', 'border': 1})
        date_format = workbook.add_format({'num_format': 'mmmm d yyyy', 'border': 1})
        sheet = workbook.add_worksheet("Income Tax")

        sheet.set_column(0, 0, 6)
        sheet.set_column(1, 1, 17)
        sheet.set_column(2, 2, 17)
        sheet.set_column(3, 3, 17)
        sheet.set_column(4, 4, 17)
        sheet.set_column(5, 5, 10)
        sheet.set_column(6, 6, 10)
        sheet.set_column(7, 7, 10)
        sheet.set_column(8, 8, 10)
        sheet.set_column(9, 9, 10)
        sheet.set_column(10, 10, 10)
        sheet.set_column(11, 11, 10)
        sheet.set_column(12, 12, 10)
        sheet.set_column(13, 13, 10)

        image_path = get_module_resource('payroll_report', 'static/src/img', 'incometax_image.png')
        image_file = open(image_path, 'rb')
        image_data = io.BytesIO(image_file.read())
        sheet.insert_image(0, 1, 'incometax_image.png', {'image_data': image_data, 'x_scale': 0.7, 'y_scale': 0.7})
        sheet.merge_range(2, 2, 3, 4, 'የኢትዮጵያ ፌዴራላዊ ዲሞክራሲዊ ሪፐብሊክ የኢትዮጵያ ገቢዎችና \n ጉምሩክ ባለስልጣን', cell_format)
        sheet.merge_range(2, 5, 2, 13, 'የሠንጠረዥ ሀ የስራ ግብር ማስታወቂ ቅፅ (ለቀጣሪዎች)', col)
        sheet.merge_range(3, 5, 3, 13, '(የገቢ ግብር አዋጅ ቁጥር 286/1996 እና ገቢ ግብር ደንብ ቁጥር 78/1994)', col)
        sheet.write(6, 0, 'ክፍል -1 የግብር ከፋይ ዝርዝር መረጃ', col0)
        if lines.company_id.owner.name != False:
            sheet.merge_range(7, 0, 7, 2, '1. የግብር ከፋይ ስም: ' + str(lines.company_id.owner.name), col)
        else:
            sheet.merge_range(7, 0, 7, 2, '1. የግብር ከፋይ ስም: ', col)
        sheet.merge_range(7, 3, 7, 5, '3. የግብር ከፋይ መለያ ቁጥር: ' + str(lines.company_id.vat), col)
        sheet.merge_range(7, 6, 7, 7, ' ', col)
        today = date.today()
        month = today.strftime("%B")
        year = today.strftime("%Y")
        sheet.write(7, 8, month, col)
        sheet.write(7, 9, year, col)
        sheet.merge_range(7, 10, 8, 13, ' ', col)

        sheet.merge_range(8, 0, 8, 1, '2a. ክልል: ' + str(lines.company_id.state_id.name), col)
        sheet.merge_range(8, 2, 8, 3, '2b. ዞን/ክፍለ  ከተማ: ' + str(lines.company_id.city), col)
        sheet.merge_range(8, 4, 8, 5, '5. የግብር ሰብሳቢ መ/ቤት ስም የኢትዮጵያ ገቢዎችና ጉምሩክ ባለስልጣን አነስተኛ ግብር ከፋዮች ቅ/ጽ/ቤት', col_wrap)
        sheet.merge_range(8, 6, 8, 7, ' ', col)
        sheet.write(8, 8, ' ', col)
        sheet.write(8, 9, ' ', col)
        sheet.merge_range(9, 0, 9, 1, '2c. ወረዳ', col)
        sheet.write(9, 2, '2d. ቀበሌ/ገበሬ ማህበር', col)
        sheet.write(9, 3, '2e. የቤት ቁጥር', col)
        sheet.merge_range(9, 4, 9, 5, '6. የስልክ ቁጥር: ' + str(lines.company_id.phone), col)
        sheet.merge_range(9, 6, 9, 7, '7. ፋክስ ቁጥር', col)
        sheet.write(9, 8, ' ', col)
        sheet.merge_range(9, 9, 9, 10, ' ', col)
        sheet.merge_range(9, 11, 9, 12, ' ', col)
        sheet.write(9, 13, ' ', col)

        topic = ['ሀ) ተ.ቁ', 'ለ) የሠራተኛው የግብር ከፋይ መለያ ቁጥር (TIN)', 'ሐ) የሠራተኛው ስም፣ የአባት ስም እና የአያት ስም',
                 'መ) የተቀጠሩበት ቀን', 'ሠ) ደመወዝ /ብር/', 'ረ) ጠቅላላ የትራንስፖርት አበል /ብር/', 'ሰ) የስራ ግብር የሚከፈልበት የትራንስፖርት አበል /ብር/',
                 'ሸ) ኮሚሽን /ብር/', 'ቀ) ሌሎች ጥቅማ ጥቅሞች /ብር/', 'በ) ጠቅላላ ግብር የሚከፈልበት ገቢ /ብር/ (ሠ+ሸ+ቀ+በ)',
                 'ተ) የስራ ግብር /ብር/', 'ቸ) ጡረታ /ብር/', 'ገ) የተጣራ ተከፋይ /ብር/', 'የሠራተኛ ፊርማ']
        sheet.write(11, 0, 'ሠንጠረዥ -2 የማስታወቂያ ዝርዝር መረጃ', col0)
        for line in range(len(topic)):
            sheet.write(12, line, topic[line], col_wrap)
        add_lis = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        line_count = 1
        col_count = 1
        row_count = 13
        trans_all = 0
        tax_trans_all = 0
        comm = 0
        net_sal = 0
        pen = 0
        gross = 0
        inc_tax = 0
        tax_inc = 0
        bas_sal = 0

        for payslip in lines:
            if payslip.contract_id.name != False:
                for line in payslip.line_ids:
                    sheet.set_row(row_count, 20)
                    if line.name == "Transportation Allowance":
                        trans_all = line.amount
                    if line.name == "Taxable Transportation Allowance":
                        tax_trans_all = line.amount
                    if line.name == "Commission":
                        comm = line.amount
                    if line.name == "Net Salary":
                        net_sal = line.amount
                    if line.name == "Pension 11%":
                        pen = line.amount
                    if line.name == "Gross":
                        gross = line.amount
                    if line.name == "Income Tax":
                        inc_tax = line.amount
                    if line.name == "Taxable Income":
                        tax_inc = line.amount
                    if line.name == "Basic Salary":
                        bas_sal = line.amount
                sheet.write(row_count, 0, line_count, col2)
                sheet.write(row_count, 1, payslip.employee_id.tin_number, col2)
                sheet.write(row_count, 2, payslip.employee_id.name, col2)
                sheet.write_datetime(row_count, 3, payslip.contract_id.date_start, date_format)
                sheet.write(row_count, 4, bas_sal, col2)
                add_lis[0] += bas_sal
                sheet.write(row_count, 5, trans_all, col2)
                add_lis[1] += trans_all
                sheet.write(row_count, 6, tax_trans_all, col2)
                add_lis[2] += tax_trans_all
                sheet.write(row_count, 7, comm, col2)
                add_lis[3] += comm
                sheet.write(row_count, 8, payslip.contract_id.other_allowance, col2)
                add_lis[4] += payslip.contract_id.other_allowance
                sheet.write(row_count, 9, gross, col2)
                add_lis[5] += gross
                sheet.write(row_count, 10, inc_tax, col2)
                add_lis[6] += inc_tax
                sheet.write(row_count, 11, pen, col2)
                add_lis[7] += pen
                sheet.write(row_count, 12, net_sal, col2)
                add_lis[8] += net_sal
            line_count += 1
            col_count += 1
            row_count += 1
        sheet.write(row_count, 0, "ድምር", col2)
        sheet.write(row_count, 1, " ", col1)
        sheet.write(row_count, 2, " ", col1)
        sheet.write(row_count, 3, " ", col1)
        for line in range(len(add_lis)):
            if add_lis[line] != 0:
                sheet.write(row_count, 4 + line, add_lis[line], col1)
            else:
                sheet.write(row_count, 4 + line, ' ', col1)


        sheet.write(row_count + 2, 0, 'ክፍል -3 የወሩ የተጠቃለለ ሂሳብ', col)
        sheet.write(row_count + 3, 0, 10, col)
        sheet.write(row_count + 3, 1, 'በዚህ ወር ደመወዝ የሚከፈላቸው የሠራተኞች ብዛት', col_wrap)
        sheet.write(row_count + 3, 2, ' ', col)
        sheet.write(row_count + 3, 3, line_count - 1, col)
        sheet.write(row_count + 4, 0, 20, col)
        sheet.write(row_count + 4, 1, 'የወሩ ጠቅላላ የሥራ ግብር የሚከፈልበት ገቢ (ከላይ ካለው ከሠንጠረዥ(በ))', col_wrap)
        sheet.write(row_count + 4, 2, ' ', col)
        sheet.write(row_count + 4, 3, add_lis[5], col)
        sheet.write(row_count + 5, 0, 30, col)
        sheet.write(row_count + 5, 1, 'የወሩ ጠቅላላ መከፈል ያለበት የሥራ ግብር (ከላይ ካለው ከሠንጠረዥ(ተ))', col_wrap)
        sheet.write(row_count + 5, 2, ' ', col)
        sheet.write(row_count + 5, 3, add_lis[6], col)

        sheet.write(row_count + 7, 0, 'ክፍል 5. የትክክለኛነት ማረጋገጫ', col0)
        sheet.merge_range(row_count + 8, 0, row_count + 8, 4, 'ከላይ የተገለፀው ማስታወቂያና የተሰጠው መረጃ በሙሉ የተሟላና ትክክለኛ መሆኑን አረጋግጣለሁ፡፡ ትክክለኛ ያልሆነ መረጃ ማቅረብ በግብር ሕጐችም ሆነ በወንጀለኛ መቅጫ ሕግ የሚያስቀጣ መሆኑን እገነዘባለሁ፡፡', col)
        sheet.merge_range(row_count + 8, 5, row_count + 8, 7, 'የግብር ከፋይ/ሕጋዊ ወኪሉ ስም ------------------------- ፊርማ --------------- ቀን ------------------------', col)
        sheet.write(row_count + 8, 8, ' ', col)
        sheet.write(row_count + 8, 9, ' ', col)
        sheet.merge_range(row_count + 8, 10, row_count + 8, 13, 'የግብር ባለሥልጣን ስም -------------------  ፊርማ ---------- ቀን --------------', col)
        sheet.write(row_count + 9, 0, 'Ethiopian Customs & Revenue Authority', col)

        sheet.set_row(2, 20)
        sheet.set_row(3, 20)
        sheet.set_row(6, 20)

        sheet.set_row(7, 40)
        sheet.set_row(8, 40)
        sheet.set_row(9, 40)

        sheet.set_row(10, 20)

        sheet.set_row(11, 20)
        sheet.set_row(12, 50)

        sheet.set_row(row_count + 1, 20)
        sheet.set_row(row_count + 2, 20)

        sheet.set_row(row_count + 3, 40)
        sheet.set_row(row_count + 4, 40)
        sheet.set_row(row_count + 5, 40)

        sheet.set_row(row_count + 6, 20)
        sheet.set_row(row_count + 7, 30)
        sheet.set_row(row_count + 8, 30)
        sheet.set_row(row_count + 9, 30)


