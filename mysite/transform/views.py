from django.http import HttpResponse
from django.template import loader
import sys
import os
sys.path.append(r'E:\master\workspace\python\gaoruan\Easy')
from Input.file import GWTFile
from Conversion.Tagging.GWTToTagged_GWT import GWTToTag
from Conversion.BranchMerge.MergeBranch import MergeBranch

def index(request):
    member_list = [{"id":"SY1706341","name":"高玉林"},{"id":"SY1706341","name":"安辽源"},{"id":"SY1706341","name":"杨明"},{"id":"SY1706341","name":"李雪桐"},{"id":"SY1706341","name":"宋立军"}]
    template = loader.get_template('transform/index.html')
    context = {
        'member_list': member_list,
    }
    return HttpResponse(template.render(context, request))


def transform(request):
    if request.method == "POST":  # 请求方法为POST时，进行处理
        myFile = request.FILES.get("theFile", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            return HttpResponse("no files for upload!")
        print(myFile.name)
        destination = open(os.path.join("G:\\upload", myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():  # 分块写入文件
            print(chunk)
            destination.write(chunk)
        destination.close()
    filepath =  os.path.join("G:\\upload", myFile.name);
    file_object = open(filepath, 'r', encoding = 'utf-8')
    try:
        file_context = file_object.readlines()
    finally:
        file_object.close()

    file = GWTFile()
    file.read_file(filepath)
    gwt_objects = file.get_gwt_objects()

    # 进行gwt转tag对象
    transformer = GWTToTag()
    tag_objects = transformer.gwtlist_to_taglist(gwt_objects)
    tag_objects[2].precondition[0].content = "收到位置传感器返回的值"
    merge_obj = MergeBranch(tag_objects)
    rucm_obj = merge_obj.rucm_obj
    rucm_obj.rucm_print()

    fps = filepath.split("\\")
    fps[-1]='RUCM_result.xls'
    rucm_obj.saveAsFile("\\".join(fps))

    template = loader.get_template('transform/result.html')
    context = {
        'GWT': file_context,
        'RUCM':rucm_obj
    }
    return HttpResponse(template.render(context, request))

#这种方式简单粗暴，适合小文件的下载，但如果这个文件非常大，这种方式会占用大量的内存，甚至导致服务器崩溃
def file_download(request):
    # do something...
    with open(os.path.join("G:\\upload", "RUCM_result.xls"),'rb') as f:
        c = f.read()
    response = HttpResponse(c)
    response['Content-Disposition'] = 'attachment; filename=RUCM.xls'
    return response