module FSM (
    input logic clk, rst, d,
    output logic detected
);

    typedef enum logic [1:0] {
        S0,  
        S1,    
        S2,
        S3   
    } state_t;

    state_t current_state, next_state;

    always_ff @(posedge clk or posedge rst) begin
        if (rst)
            current_state <= S0;
        else
            current_state <= next_state;
    end
    
    // assign detected=current_state==S3? 1: 0;
    
    always_comb begin
        next_state=current_state; 
        case (current_state)
            S0: begin
                if (d) begin 
                    next_state = S1;
                    detected = 0;
                end
                else begin
                    next_state = S0;
                    detected = 0;
                end
            end
            S1: begin
                if (!d) begin
                    next_state = S2;
                    detected = 0;
                end
                else begin
                    next_state=S1;  
                    detected = 0;
                end
            end
            S2: begin
                if (d) begin 
                    next_state = S3;  
                    detected = 1;
                end
                else begin 
                    next_state = S0;   
                    detected = 0;
                end
            end
            S3: begin
                if(d) begin 
                    next_state=S1;
                    detected = 0;
                end
                else begin
                    next_state=S2;
                    detected = 0;
                end
            end
        endcase
    end
    
    initial begin
        $dumpfile("dump.vcd");
        $dumpvars(1, FSM);
    end

endmodule
