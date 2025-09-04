create database project;
use project;

create table publisher (publisher_PublisherName varchar(100) primary key,
					  publisher_PublisherAddress varchar(255),
                      publisher_PublisherPhone varchar(100));
                        
select * from publisher;




create table borrower (borrower_CardNo tinyint primary key ,
						borrower_BorrowerName varchar(100),
                        borrower_BorrowerAddress varchar (100),
                        borrower_BorrowerPhone varchar(100));
                        


select * from borrower;

create table library_branch(library_branch_BranchID tinyint auto_increment primary key,
						   library_branch_BranchName varchar(150),
                           library_branch_BranchAddress varchar(150));
                           
select * from library_branch;


create table books(book_BookID tinyint primary key,
					book_title varchar(255),
                    book_PublisherName varchar(100),
                    foreign key(book_PublisherName) references publisher(publisher_PublisherName));

select * from books;


create table book_loans(book_loans_LoansID tinyint auto_increment primary key,
					     book_loans_BookID tinyint,
                         book_loans_BranchID tinyint ,
                         book_loans_CardNo tinyint,
                         books_loans_DateOut varchar(100),
                         book_loans_DueDate varchar(100),
                         foreign key(book_loans_BookID)references books(book_BookID),
                         foreign key(book_loans_BranchID)references library_branch(library_branch_BranchID),
                         foreign key(book_loans_CardNo) references borrower(borrower_CardNo));
                         
                         
select * from book_loans;        


create table book_authors(book_authors_AuthorID tinyint auto_increment primary key,
								 book_authors_BookID tinyint,
                                 book_author_AuthorName varchar(150),
                                 foreign key(book_authors_BookID) references books(book_BookID));
                                 
                                 
                                 
select * from book_authors;
        
        
        
create table book_copies(book_copies_CopiesID tinyint auto_increment primary key,
						book_copies_BookID tinyint,
                        book_copies_BranchID tinyint,
                        book_copies_No_Of_Copies tinyint,
                        foreign key(book_copies_BookID) references books(book_BookID),
                        foreign key(book_copies_BranchID) references library_branch(library_branch_BranchID));
                        
select * from book_copies;


select * from publisher;
select * from borrower;
select * from library_branch;
select * from books;
select * from book_loans;
select * from book_authors;
select * from book_copies;


-- 1.How many copies of the book titled "The Lost Tribe" are owned by the library branch whose name is "Sharpstown"? 


select b.book_title,l.library_branch_BranchName,bc.book_copies_No_Of_Copies from books b
		inner join book_copies bc
        on b.book_BookID=bc.book_copies_BookID
        inner join library_branch l
        on l.library_branch_Branchid=bc.book_copies_BranchID
        where book_title="The Lost Tribe" and library_branch_BranchName="Sharpstown";
        
        
        
        
-- 2.How many copies of the book titled "The Lost Tribe" are owned by each library branch?

select b.book_title,l.library_branch_BranchName,bc.book_copies_No_Of_Copies from books b
		inner join book_copies bc
        on b.book_BookID=bc.book_copies_BookID
        inner join library_branch l
        on l.library_branch_Branchid=bc.book_copies_BranchID
        where book_title="The Lost Tribe";
        
        
        
        
-- 3.Retrieve the names of all borrowers who do not have any books checked out.

select * from borrower br 
		left join book_loans bl
        on br.borrower_CardNo=bl.book_loans_CardNo
       where book_loans_CardNo is null;
        
        
        
        
        




-- 4.For each book that is loaned out from the "Sharpstown" branch and whose DueDate is 2/3/18, retrieve the book title, the borrower's name, and the borrower's address.?

select lb.library_branch_BranchName,b.book_title,br.borrower_BorrowerName,br.borrower_BorrowerAddress,bl.book_loans_DueDate from borrower br 
		inner join book_loans bl
        on br.borrower_CardNo=bl.book_loans_CardNo
        inner join books b
        on b.book_BookID=bl.book_loans_BookID
        inner join library_branch lb
        on lb.library_branch_BranchID=bl.book_loans_BranchID
        where book_loans_DueDate="2/3/18" and library_branch_BranchName="sharpstown";
        




-- 5. For each library branch, retrieve the branch name and the total number of books loaned out from that branch.

select library_branch_BranchName,sum(case when book_loans_BookID is not null then 1 else 0 end) as total_books_loaned_out from library_branch lb
		inner join book_loans bl
        on lb.library_branch_BranchID=bl.book_loans_BranchID
        group by library_branch_BranchName;



-- 6. Retrieve the names, addresses, and number of books checked out for all borrowers who have more than five books checked out.
select borrower_BorrowerName,borrower_BorrowerAddress,count(book_loans_CardNo)as count_of_books  from borrower br 
		left  join book_loans bl
        on br.borrower_CardNo=bl.book_loans_CardNo
          group by borrower_BorrowerName,borrower_BorrowerAddress
          having count(book_loans_CardNo)>5
          order by count_of_books desc;
        
        
        



-- 7. For each book authored by "Stephen King", retrieve the title and the number of copies owned by the library branch whose name is "Central".

select ba.book_author_AuthorName,b.book_title,bc.book_copies_No_Of_Copies,lb.library_branch_BranchName from book_authors ba
		inner join books b
        on ba.book_authors_BookID=b.book_BookID
        inner join book_copies bc
        on b.book_BookID=bc.book_copies_BookID
        inner join library_branch lb
        on bc.book_copies_BranchID=lb.library_branch_BranchID
        where book_author_AuthorName = "Stephen King" and library_branch_BranchName="Central";