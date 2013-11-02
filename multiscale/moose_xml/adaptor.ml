<?xml version="1.0"?>
<adapterML>
<listOfAdaptors>
        <adaptor name="adaptK" id="/n/chem/neuroMesh/adaptK" scale="0.05">
                <inElement name="chemK" id="/n/chem/neuroMesh/kChan" field="get_conc" adapt_type="requestField" mode="OneToAll"/>
                <outElement name="elecK" id="/n/elec/compt/K" field="set_Gbar" adapt_type="outputSrc" mode="OneToAll"/>
        </adaptor>

        <adaptor name="adaptCa" id="/n/chem/neuroMesh/adaptCa" outputOffset="0.0001" scale="0.05">
                <inElement name="elecCa" id="/n/elec/compt/ca" field="concOut" adapt_type="input" mode="OneToAll"/>
                <outElement name="chemCa" id="/n/chem/neuroMesh/Ca" field="set_conc" adapt_type="outputSrc" mode="OneToAll"/>
        </adaptor>

</listOfAdaptors>
</adapterML>
