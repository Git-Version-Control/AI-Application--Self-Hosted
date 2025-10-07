from danToEng import DanToEngTranslator
from engToDan import EngToDanTranslator
llmDan = DanToEngTranslator()
llmEng = EngToDanTranslator()
print(llmEng("slufuric acid fell on my hand"))
# print(llmDan("Beklager, jeg ved ikke om dette. Giv venligst mere kontekst eller oplysninger om det scenario, du henviser til, så jeg kan hjælpe dig bedre. Mente du svovlsyre? Hvis ja, Bemærk venligst, at det er et meget ætsende og giftigt stof, der kan forårsage alvorlige forbrændinger og øjenskader ved kontakt med hud eller øjne. Det er vigtigt at håndtere svovlsyre med forsigtighed og bære passende beskyttende tøj, herunder handsker, sikkerhedsbriller, og et ansigtsskjold. Hvis du ved et uheld har spildt svovlsyre på din hånd, bedes du søge lægehjælp straks."))