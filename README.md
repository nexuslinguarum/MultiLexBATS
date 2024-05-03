# MultiLexBATS
The Multilingual Lexical BATS datasets comprises lexical semantic relations in 15 natural languages listed in the table below. 

The dataset folder contains a folder "all_languages" with ID- and English-aligned columns for each contained languages. Additionally, MultiLexBATS is also provided as individual language files with one folder and all relations files for each language in the dataset folder.

All scripts used in this experiments, e.g. for running statistics on the dataset (folder "stats") or querying generative pre-trained transformers i.e., <a href="https://huggingface.co/bigscience/bloom">BLOOM</a> via the HuggingFace Interface API, are provided in the "scripts" folder. 

For the languages that correspond to MATS languages, we utilised the same templates as in MATS. For all other languages, first language speakers created templates. For languages where there is not a direct equivalence to the English template, first language speakers proposed several templates that we tested. Please consult the final paper on which templates performed best in the experiments.

<table>
    <tr>
        <td>Language</td>
        <td>Prompt</td>
    </tr>
    <tr>
        <td>EN</td>
        <td>``&lt;a&gt;&#39;&#39; is to ``&lt;b&gt;&#39;&#39; as ``&lt;c&gt;&#39;&#39; is to ``&lt;d&gt;&#39;&#39;.</td>
    </tr>
    <tr>
        <td>AL</td>
        <td>``&lt;a&gt;&#39;&#39; është për ``&lt;b&gt;&#39;&#39; ashtu si ``&lt;c&gt;&#39;&#39; për ``&lt;d&gt;&#39;&#39;.</td>
    </tr>
    <tr>
        <td>BM</td>
        <td>``&lt;a&gt;&#39;&#39; ye ``&lt;b&gt;&#39;&#39; ye i n’a fɔ ``&lt;c&gt;&#39;&#39; ye ``&lt;d&gt;&#39;&#39; ye</td>
    </tr>
    <tr>
        <td>DE</td>
        <td>``&lt;a&gt;&#39;&#39; ist so zu ``&lt;b&gt;&#39;&#39; wie ``&lt;c&gt;&#39;&#39; zu &lt;d&gt; ist.</td>
    </tr>
    <tr>
        <td>EL</td>
        <td>το ``&lt;a&gt;&#39;&#39; είναι προς το ``&lt;b&gt;&#39;&#39; ό,τι το ``&lt;c&gt;&#39;&#39; προς το ``&lt;d&gt;&#39;&#39;.</td>
    </tr>
    <tr>
        <td>ES</td>
        <td>``&lt;a&gt;&#39;&#39; es a``&lt;b&gt;&#39;&#39;como ``&lt;c&gt;&#39;&#39; es a ``&lt;d&gt;&#39;&#39;.</td>
    </tr>
    <tr>
        <td>FR</td>
        <td>``&lt;a&gt;&#39;&#39; est à ``&lt;b&gt;&#39;&#39; ce que ``&lt;c&gt;&#39;&#39; est à ``&lt;d&gt;&#39;&#39;.</td>
    </tr>
    <tr>
        <td>HE</td>
        <td>``&lt;a&gt;&#39;&#39; ל ``&lt;b&gt;&#39;&#39; כ ``&lt;c&gt;&#39;&#39; ל ``&lt;d&gt;&#39;&#39;</td>
    </tr>
    <tr>
        <td>HR1</td>
        <td>``&lt;a&gt;&#39;&#39; je za ``&lt;b&gt;&#39;&#39; kao što je ``&lt;c&gt;&#39;&#39; za ``&lt;d&gt;&#39;&#39;.</td>
    </tr>
    <tr>
        <td>HR2</td>
        <td>Riječ ``&lt;a&gt;&#39;&#39; je riječi ``&lt;b&gt;&#39;&#39; jednako što je riječ ``&lt;c&gt;&#39;&#39; riječi ``&lt;d&gt;&#39;&#39;.</td>
    </tr>
    <tr>
        <td>HR3</td>
        <td>Odnos između riječi ``&lt;a&gt;&#39;&#39; i ``&lt;b&gt;&#39;&#39; jednak je odnosu između riječi ``&lt;c&gt;&#39;&#39; i ``&lt;d&gt;&#39;&#39;.</td>
    </tr>
    <tr>
        <td>IT</td>
        <td>``&lt;a&gt;&#39;&#39;  sta a ``&lt;b&gt;&#39;&#39; come ``&lt;c&gt;&#39;&#39; sta a ``&lt;d&gt;&#39;&#39;.</td>
    </tr>
    <tr>
        <td>LT</td>
        <td>``&lt;a&gt;&#39;&#39; yra ``&lt;b&gt;&#39;&#39; taip, kaip ``&lt;c&gt;&#39;&#39; yra ``&lt;d&gt;&#39;&#39;.</td>
    </tr>
    <tr>
        <td>MK1</td>
        <td>``&lt;a&gt;&#39;&#39; е за ``&lt;b&gt;&#39;&#39; исто што и ``&lt;c&gt;&#39;&#39; за ``&lt;d&gt;&#39;&#39;.</td>
    </tr>
    <tr>
        <td>MK2</td>
        <td>Зборот ``&lt;a&gt;&#39;&#39; за зборот ``&lt;b&gt;&#39;&#39; е исто што и зборот ``&lt;c&gt;&#39;&#39; за зборот ``&lt;d&gt;&#39;&#39;.</td>
    </tr>
    <tr>
        <td>MK3</td>
        <td>Односот меѓу зборовите  ``&lt;a&gt;&#39;&#39; и ``&lt;b&gt;&#39;&#39; е еднаков со односот меѓу зборовите ``&lt;c&gt;&#39;&#39; и ``&lt;d&gt;&#39;&#39;.</td>
    </tr>
    <tr>
        <td>PT</td>
        <td>``&lt;a&gt;&#39;&#39; está para ``&lt;b&gt;&#39;&#39; assim como ``&lt;c&gt;&#39;&#39; está para ``&lt;d&gt;&#39;&#39;.</td>
    </tr>
    <tr>
        <td>RO</td>
        <td>``&lt;a&gt;&#39;&#39; este pentru ``&lt;b&gt;&#39;&#39; cum ``&lt;c&gt;&#39;&#39; este pentru ``&lt;d&gt;&#39;&#39;.</td>
    </tr>
    <tr>
        <td>SK1</td>
        <td>Slovo ``&lt;a&gt;&#39;&#39; sa má k slovu ``&lt;b&gt;&#39;&#39; ako slovo ``&lt;c&gt;&#39;&#39; k slovu ``&lt;d&gt;&#39;&#39;.</td>
    </tr>
    <tr>
        <td>SK2</td>
        <td>Vzťah medzi slovami ``&lt;a&gt;&#39;&#39; a ``&lt;b&gt;&#39;&#39; je rovnaký ako medzi ``&lt;c&gt;&#39;&#39; a ``&lt;d&gt;&#39;&#39;.</td>
    </tr>
    <tr>
        <td>SK3</td>
        <td>``&lt;a&gt;&#39;&#39; sa má k ``&lt;b&gt;&#39;&#39; ako ``&lt;c&gt;&#39;&#39; k ``&lt;d&gt;&#39;&#39;.</td>
    </tr>
    <tr>
        <td>SL1</td>
        <td>Beseda ``&lt;a&gt;&#39;&#39; je besedi ``&lt;b&gt;&#39;&#39; enako, kot je beseda ``&lt;c&gt;&#39;&#39; besedi ``&lt;d&gt;&#39;&#39;.</td>
    </tr>
    <tr>
        <td>SL2</td>
        <td>Beseda ``&lt;a&gt;&#39;&#39; je besedi ``&lt;b&gt;&#39;&#39; enako, kot je besedi ``&lt;d&gt;&#39;&#39; beseda ``&lt;c&gt;&#39;&#39;.</td>
    </tr>
    <tr>
        <td>SL3</td>
        <td>``&lt;a&gt;&#39;&#39; in ``&lt;b&gt;&#39;&#39; sta kot ``&lt;c&gt;&#39;&#39; in ``&lt;d&gt;&#39;&#39;.</td>
    </tr>
</table>

Detailed results on analogy completion with the above templates as well as translation prediction with XLM-R and mBERT are provided in the LREC submission. 

The detailed results achieved on analogy completion with BLOOM are reported in the following table, where only an overview graphic is included in the LREC submission. 

<table>
    <tr>
        <td>  </td>
        <td> L01 hypern - animals </td>
        <td> L02 hypern - misc </td>
        <td> L03 hyponyms - misc </td>
        <td> L04 meronyms - substance </td>
        <td> L05 meronyms - member </td>
        <td> L06 meronyms - part </td>
        <td> L07 synonyms - intensity </td>
        <td> L08 synonyms - exact </td>
        <td> L09 antonyms - gradable </td>
        <td> L10 antonyms - binary </td>
        <td> Total </td>
    </tr>
    <tr>
        <td> EN </td>
        <td> 0.70 </td>
        <td> 0.60 </td>
        <td> 0.30 </td>
        <td> 0.40 </td>
        <td> 0.26 </td>
        <td> 0.23 </td>
        <td> 0.23 </td>
        <td> 0.27 </td>
        <td> 0.40 </td>
        <td> 0.73 </td>
        <td> 0.41 </td>
    </tr>
    <tr>
        <td> AL </td>
        <td> 0.33 </td>
        <td> 0.50 </td>
        <td> 0.37 </td>
        <td> 0.27 </td>
        <td> 0.07 </td>
        <td> 0.10 </td>
        <td> 0.07 </td>
        <td> 0.10 </td>
        <td> 0.10 </td>
        <td> 0.07 </td>
        <td> 0.20 </td>
    </tr>
    <tr>
        <td> BM </td>
        <td> 0.13 </td>
        <td> 0.13 </td>
        <td> 0.17 </td>
        <td> 0.23 </td>
        <td> 0.03 </td>
        <td> 0.23 </td>
        <td> 0.07 </td>
        <td> 0.10 </td>
        <td> 0.03 </td>
        <td> 0.03 </td>
        <td> 0.12 </td>
    </tr>
    <tr>
        <td> DE </td>
        <td> 0.47 </td>
        <td> 0.57 </td>
        <td> 0.13 </td>
        <td> 0.30 </td>
        <td> 0.10 </td>
        <td> 0.33 </td>
        <td> 0.03 </td>
        <td> 0.13 </td>
        <td> 0.07 </td>
        <td> 0.27 </td>
        <td> 0.24 </td>
    </tr>
    <tr>
        <td> EL </td>
        <td> 0.40 </td>
        <td> 0.17 </td>
        <td> 0.13 </td>
        <td> 0.07 </td>
        <td> 0.07 </td>
        <td> 0.10 </td>
        <td> 0.10 </td>
        <td> 0.13 </td>
        <td> 0.13 </td>
        <td> 0.33 </td>
        <td> 0.16 </td>
    </tr>
    <tr>
        <td> ES </td>
        <td> 0.90 </td>
        <td> 0.53 </td>
        <td> 0.27 </td>
        <td> 0.33 </td>
        <td> 0.20 </td>
        <td> 0.20 </td>
        <td> 0.10 </td>
        <td> 0.13 </td>
        <td> 0.30 </td>
        <td> 0.47 </td>
        <td> 0.34 </td>
    </tr>
    <tr>
        <td> FR </td>
        <td> 0.77 </td>
        <td> 0.50 </td>
        <td> 0.33 </td>
        <td> 0.57 </td>
        <td> 0.17 </td>
        <td> 0.20 </td>
        <td> 0.00 </td>
        <td> 0.23 </td>
        <td> 0.23 </td>
        <td> 0.50 </td>
        <td> 0.35 </td>
    </tr>
    <tr>
        <td> HE </td>
        <td> 0.17 </td>
        <td> 0.17 </td>
        <td> 0.10 </td>
        <td> 0.10 </td>
        <td> 0.03 </td>
        <td> 0.10 </td>
        <td> 0.10 </td>
        <td> 0.07 </td>
        <td> 0.13 </td>
        <td> 0.10 </td>
        <td> 0.11 </td>
    </tr>
    <tr>
        <td> HR </td>
        <td> 0.40 </td>
        <td> 0.30 </td>
        <td> 0.03 </td>
        <td> 0.33 </td>
        <td> 0.07 </td>
        <td> 0.13 </td>
        <td> 0.03 </td>
        <td> 0.17 </td>
        <td> 0.03 </td>
        <td> 0.13 </td>
        <td> 0.16 </td>
    </tr>
    <tr>
        <td> IT </td>
        <td> 0.60 </td>
        <td> 0.67 </td>
        <td> 0.17 </td>
        <td> 0.23 </td>
        <td> 0.07 </td>
        <td> 0.13 </td>
        <td> 0.13 </td>
        <td> 0.13 </td>
        <td> 0.17 </td>
        <td> 0.47 </td>
        <td> 0.28 </td>
    </tr>
    <tr>
        <td> LT </td>
        <td> 0.40 </td>
        <td> 0.37 </td>
        <td> 0.03 </td>
        <td> 0.03 </td>
        <td> 0.07 </td>
        <td> 0.10 </td>
        <td> 0.10 </td>
        <td> 0.07 </td>
        <td> 0.07 </td>
        <td> 0.10 </td>
        <td> 0.13 </td>
    </tr>
    <tr>
        <td> MK </td>
        <td> 0.37 </td>
        <td> 0.47 </td>
        <td> - </td>
        <td> 0.10 </td>
        <td> 0.03 </td>
        <td> - </td>
        <td> 0.10 </td>
        <td> 0.07 </td>
        <td> - </td>
        <td> 0.23 </td>
        <td> 0.20 </td>
    </tr>
    <tr>
        <td> PT </td>
        <td> 0.60 </td>
        <td> 0.57 </td>
        <td> 0.17 </td>
        <td> 0.36 </td>
        <td> 0.10 </td>
        <td> 0.33 </td>
        <td> 0.13 </td>
        <td> 0.20 </td>
        <td> 0.40 </td>
        <td> 0.70 </td>
        <td> 0.36 </td>
    </tr>
    <tr>
        <td> SL </td>
        <td> 0.36 </td>
        <td> 0.33 </td>
        <td> 0.07 </td>
        <td> 0.30 </td>
        <td> 0.10 </td>
        <td> 0.17 </td>
        <td> 0.10 </td>
        <td> 0.07 </td>
        <td> 0.10 </td>
        <td> 0.13 </td>
        <td> 0.17 </td>
    </tr>
    <tr>
        <td> SK </td>
        <td> 0.33 </td>
        <td> 0.47 </td>
        <td> 0.13 </td>
        <td> 0.13 </td>
        <td> 0.07 </td>
        <td> 0.10 </td>
        <td> 0.10 </td>
        <td> 0.23 </td>
        <td> 0.17 </td>
        <td> 0.23 </td>
        <td> 0.20 </td>
    </tr>
    <tr>
        <td> RO </td>
        <td> 0.27 </td>
        <td> 0.57 </td>
        <td> 0.13 </td>
        <td> 0.13 </td>
        <td> 0.03 </td>
        <td> 0.07 </td>
        <td> 0.17 </td>
        <td> 0.13 </td>
        <td> 0.10 </td>
        <td> 0.10 </td>
        <td> 0.17 </td>
    </tr>
    <tr>
        <td> Total </td>
        <td> 0.45 </td>
        <td> 0.43 </td>
        <td> 0.17 </td>
        <td> 0.24 </td>
        <td> 0.09 </td>
        <td> 0.17 </td>
        <td> 0.10 </td>
        <td> 0.14 </td>
        <td> 0.16 </td>
        <td> 0.29 </td>
        <td> 0.22 </td>
    </tr>
</table>
