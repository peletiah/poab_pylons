def timediff(deltaseconds):
    deltahours=int(deltaseconds/3600) #full hours(integer only, no partial hours)
    deltaminutes=int((deltaseconds-int(deltahours)*3600)/60)
    if deltaseconds < 0:
        prefix='-'
    elif deltaseconds > 0:
        prefix='+'
    else:
        prefix='&plusmn; 0 hours'

    if deltahours == 0:
        hourstring=''
    elif deltahours > 1:
        hourstring=str(deltahours)+' hours '
    elif deltahours < -1:
        hourstring=str(deltahours).replace('-','')+' hours '
    elif deltahours > 0:
        hourstring=str(deltahours)+' hour '
    elif deltahours < 0:
        hourstring=str(deltahours).replace('-','')+' hour '

    if deltaminutes == 0:
        minutestring=''
    elif deltaminutes < 0:
        minutestring=str(deltaminutes).replace('-','')+' minutes'
    elif deltaminutes > 0:
        minutestring=str(deltaminutes)+' minutes'

    timediff='UTC'+prefix+hourstring+minutestring
    return timediff

