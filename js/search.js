function runSearch( term ) {
    $('#results').hide();
    $('tbody').empty();
    
    var frmStr = $('#gene_search').serialize();
    
    $.ajax({
        url: './ucscpractice.cgi',
        dataType: 'json',
        data: frmStr,
        success: function(data, textStatus, jqXHR) {
            processJSON(data);
        },
        error: function(jqXHR, textStatus, errorThrown){
            alert("Failed to perform gene search! textStatus: (" + textStatus +
                  ") and errorThrown: (" + errorThrown + ")");
        }
    });
}

function processJSON( data ) {
    $('#match_count').text( data.match_count );
    
    var next_row_num = 1;
    $.each( data.matches, function(i, item) {
        var this_row_id = 'result_row_' + next_row_num++;
    
       
        $('<tr/>', { "id" : this_row_id } ).appendTo('tbody');
        
    
        $('<td/>', { "text" : item.chrom } ).appendTo('#' + this_row_id);
        $('<td/>', { "text" : item.txStart } ).appendTo('#' + this_row_id);
        $('<td/>', { "text" : item.txEnd } ).appendTo('#' + this_row_id);
        $('<td/>', { "text" : item.geneSymbol } ).appendTo('#' + this_row_id);
        $('<td/>', { "text" : item.score } ).appendTo('#' + this_row_id);
        $('<td/>', { "text" : item.strand } ).appendTo('#' + this_row_id);
        $('<td/>', { "text" : item.cdsStart } ).appendTo('#' + this_row_id);
        $('<td/>', { "text" : item.cdsEnd } ).appendTo('#' + this_row_id);
        $('<td/>', { "text" : item.rgb } ).appendTo('#' + this_row_id);
        $('<td/>', { "text" : item.exonCount } ).appendTo('#' + this_row_id);
        $('<td/>', { "text" : item.exonsizes } ).appendTo('#' + this_row_id);
        $('<td/>', { "text" : item.exonStarts } ).appendTo('#' + this_row_id);
    });
    
    
    $('#results').show();
}


$(document).ready( function() {
    
    $('#submit').click( function() {
        runSearch();
        return false;  
    });

    $("#bed_download").on('click', function() {
        window.location.href = "./ucscpractice_text.cgi?" +  $('#gene_search').serialize();
    });

});
