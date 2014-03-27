outputFileName="/tmp/HCSO_results.txt"
tmpFile="/tmp/HCSO.txt"
wget http://apps.hcso.org/PropertySale.aspx -O "${tmpFile}"

viewState=$( grep VIEWSTATE ${tmpFile} |  sed 's/.*value="//;s/".*//' )


tsm_HiddenField="8jSHtPUq5GTpTU7TqyBMDISfz_eSpI82sxIw_rAiXhI1"
eventTarget=""
eventArgument=""


viewStateEncrypted="" #_VIEWSTATEENCRYPTED" value="" />
eventValidation=$( grep EVENTVALIDATION ${tmpFile} |  sed 's/.*value="//;s/".*//' ) #needed?

echo $viewState
echo ""
echo $eventValidation

ddlDate="5/1/2014"
ddlTown=""
txtAddress=""
btnCurrent="Upcoming Foreclosures"
txtCaseno=""
txtAddress=""
btnGo="GO"
curl -d "txtAddress=${txtAddress}&txtCaseno=${txtCaseno}&ddlDate=${ddlDate}&ddlTown=${ddlTown}&__EVENTVALIDATION=${eventValidation}&__VIEWSTATEENCRYPTED=${viewStateEncrypted}&__EVENTTARGET=${eventTarget}&__EVENTARGUMENT=${eventArgument}&_TSM_HiddenField=${tsm_HiddenField}__VIEWSTATE=${viewState}&txtAddress_TextBoxWatermarkExtender_ClientState=${txtAddress}&btnCurrent=${btnCurrent}&btnGo=${btnGo}" http://apps.hcso.org/PropertySale.aspx > "${outputFileName}"

#curl -d "__EVENTVALIDATION=${eventValidation}&__VIEWSTATEENCRYPTED=${viewStateEncrypted}&__EVENTTARGET=${eventTarget}&__EVENTARGUMENT=${eventArgument}&_TSM_HiddenField=${tsm_HiddenField}__VIEWSTATEENCRYPTED=${viewStateEncrypted}&txtAddress_TextBoxWatermarkExtender_ClientState=${txtAddress}&btnCurrent=${btnCurrent}" http://apps.hcso.org/PropertySale.aspx > "${outputFileName}"

#curl -d "ddlDate=${ddlDate}&ddlTown=${ddlTown}" http://apps.hcso.org/PropertySale.aspx > "${outputFileName}"

#curl -d "ddlDate=${ddlDate}&ddlTown=${ddlTown}" http://apps.hcso.org/PropertySale.aspx > "${outputFileName}"

